import os
from functools import partial
from datetime import datetime, timedelta
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_mail import Message

from common.forms import NewOrder, NewebPayForm
from models import CartItem, Product, Order, OrderItem, OrderStatus, PaymentStatus, ShippingStatus
from models.user.decorators import require_login
from common.constant import USER, CART_ID
from common.flash_message import product_not_found, order_not_found, order_complete, order_cannot_modify
from common.generate_many_flash_message import generate_many_flash_message
from helpers.orders_view_helper import get_order_data, get_trade_info, get_trade_sha
from app import mail

order_blueprint = Blueprint('orders', __name__)
flash_warning_messages = partial(generate_many_flash_message, category='warning')


@order_blueprint.route('/order_item/<string:seller_id>', methods=['POST'])
@require_login
def new_order_item(seller_id):
    # save cart_item to order_item table, then clean cart_item
    if not seller_id.isnumeric():
        flash(*product_not_found)
        return url_for('carts.get_cart_items')

    amount = 0
    order = Order(
        amount=0,
        recipient=session.get(USER).get('display_name'),
        cell_phone=session.get(USER).get('cell_phone') or 'None',
        address=session.get(USER).get('address') or 'None',
        shipping_status_id=1,  # 未出貨
        payment_status_id=1,  # 未付款
        order_status_id=1,  # 未結帳
        seller_id=seller_id,
        buyer_id=session.get(USER).get('id')
    )
    order.save_to_db()

    cart_items = CartItem.query \
        .join(Product) \
        .filter(CartItem.cart_id == session.get(USER).get(CART_ID)) \
        .filter(Product.seller_id == seller_id) \
        .all()

    if not cart_items:
        flash(*product_not_found)
        return url_for('carts.get_cart_items')

    for item in cart_items:
        amount += item.product.price * item.quantity
        OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            name=item.product.name,
            price=item.product.price,
            image_url=item.product.image_url,
            quantity=item.quantity
        ).save_to_db()
        item.delete()

    order.amount = amount
    order.save_to_db()
    return redirect(url_for('.new_order', order_id=str(order.id)))


@order_blueprint.route('/new/<string:order_id>', methods=['GET', 'POST'])
@require_login
def new_order(order_id):
    # validate request
    if not order_id.isnumeric():
        flash(*order_not_found)
        return redirect(url_for('carts.get_cart_items'))

    order = Order.find_by_id(order_id)
    if order.buyer_id != session.get(USER).get('id'):
        flash(*order_not_found)
        return redirect(url_for('carts.get_cart_items'))

    if not order:
        flash(*order_not_found)
        return redirect(url_for('carts.get_cart_items'))

    if order.order_status_id == 2 or order.order_status_id == 4:
        flash(*order_cannot_modify)
        return redirect(url_for('carts.get_cart_items'))

    row = OrderItem.query \
        .with_entities(OrderItem.price, OrderItem.quantity, OrderItem.image_url, OrderItem.name) \
        .filter(OrderItem.order_id == order_id) \
        .all()

    if not row:
        flash(*order_not_found)
        return redirect(url_for('carts.get_cart_items'))

    amount = f'{order.amount:,}'
    order_items = []
    for data in row:
        order_items.append({
            'price': f'{data.price:,}',
            'quantity': data.quantity,
            'subtotal': f'{data.price * data.quantity:,}',
            'image_url': data.image_url,
            'name': data.name
        })

    form = NewOrder()

    if request.method == 'GET':
        # user can check order
        form.recipient.data = order.recipient
        form.cell_phone.data = order.cell_phone if order.cell_phone != 'None' else None
        form.address.data = order.address if order.address != 'None' else None

    else:
        # user can checkout order
        if form.validate_on_submit():
            order.recipient = form.recipient.data
            order.cell_phone = form.cell_phone.data
            order.address = form.address.data
            order.order_status_id = 2  # 已結帳
            order.save_to_db()

            flash(*order_complete)
            msg = Message(
                subject='牙牙商城訂單已結帳',
                recipients=[session.get(USER).get('email')],
                html=f'<p>訂單已結帳。<a href="{request.url_root}orders/{order_id}">訂單明細連結</a></p>'
            )
            mail.send(msg)

            return redirect(url_for('.get_orders'))

        else:
            flash_warning_messages(form.recipient.errors)
            flash_warning_messages(form.cell_phone.errors)
            flash_warning_messages(form.address.errors)

    return render_template('orders/new.html', form=form, order_id=order_id, order_items=order_items, amount=amount)


@order_blueprint.route('/')
@require_login
def get_orders():
    two_year_ago = datetime.now() - timedelta(days=732)
    buy_order_row = Order.query \
        .with_entities(Order, OrderStatus.status, PaymentStatus.status, ShippingStatus.status) \
        .join(OrderStatus) \
        .join(PaymentStatus) \
        .join(ShippingStatus) \
        .join(OrderItem) \
        .filter(Order.buyer_id == session.get(USER).get('id')) \
        .filter(Order.update_time >= two_year_ago) \
        .order_by(Order.update_time.desc()) \
        .all()

    buy_orders = []
    for data in buy_order_row:
        buy_orders.append({
            'order_id': data.Order.id,
            'amount': f'{data.Order.amount:,}',
            'update_time': datetime.strftime(data.Order.update_time, '%Y-%m-%d'),
            'order_status': data[1],
            'payment_status': data[2],
            'shipping_status': data[3]
        })

    sell_order_row = Order.query \
        .with_entities(Order, OrderStatus.status, PaymentStatus.status, ShippingStatus.status) \
        .join(OrderStatus) \
        .join(PaymentStatus) \
        .join(ShippingStatus) \
        .join(OrderItem) \
        .filter(Order.seller_id == session.get(USER).get('id')) \
        .filter(Order.update_time >= two_year_ago) \
        .order_by(Order.update_time.desc()) \
        .all()

    sell_orders = []
    for data in sell_order_row:
        sell_orders.append({
            'order_id': data.Order.id,
            'amount': f'{data.Order.amount:,}',
            'update_time': datetime.strftime(data.Order.update_time, '%Y-%m-%d'),
            'order_status': data[1],
            'payment_status': data[2],
            'shipping_status': data[3]
        })

    return render_template('orders/orders.html', buy_orders=buy_orders, sell_orders=sell_orders)


@order_blueprint.route('/<string:order_id>')
@require_login
def get_order(order_id):
    if not order_id.isnumeric():
        flash(*order_not_found)
        return redirect(url_for('.get_orders'))

    user_id = session.get(USER).get('id')
    order = get_order_data(order_id, user_id)

    if order is None:
        flash(*order_not_found)
        return redirect(url_for('.get_orders'))

    return render_template('orders/order.html', order=order, user_id=user_id)


@order_blueprint.route('/payment/<string:order_id>')
@require_login
def pay_order(order_id):
    if not order_id.isnumeric():
        flash(*order_not_found)
        return redirect(url_for('.get_orders'))

    user_id = session.get(USER).get('id')
    order = get_order_data(order_id, user_id)

    if order is None:
        flash(*order_not_found)
        return redirect(url_for('.get_orders'))

    # 藍新金流Newebpay_MPG串接手冊_MPG_1.1.1 page 33-38
    form = NewebPayForm()
    trade_info = get_trade_info(
        order_id=order_id,
        amount=order['amount_int'],
        email=session.get(USER).get('email')
    )
    form.MerchantID.data = os.environ.get('MerchantID')
    form.TradeInfo.data = trade_info
    form.TradeSha.data = get_trade_sha(trade_info)
    form.Version.data = 1.6

    FormName = 'Newebpay'
    FormAction = 'https://ccore.newebpay.com/MPG/mpg_gateway'

    return render_template('orders/payment.html', form=form, order=order, FormName=FormName, FormAction=FormAction)
