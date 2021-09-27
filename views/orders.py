from functools import partial
from datetime import datetime, timedelta
from flask import Blueprint, render_template, session, redirect, url_for, flash, request

from common.forms import NewOrder
from models import CartItem, Product, Order, OrderItem, OrderStatus, PaymentStatus, ShippingStatus
from models.user.decorators import require_login
from common.constant import USER, CART_ID
from common.flash_message import product_not_found, order_not_found, order_complete, order_cannot_modify
from common.generate_many_flash_message import generate_many_flash_message

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
    row = Order.query \
        .with_entities(Order, OrderItem, OrderStatus.status, PaymentStatus.status, ShippingStatus.status) \
        .join(OrderItem) \
        .join(OrderStatus) \
        .join(PaymentStatus) \
        .join(ShippingStatus) \
        .filter(Order.id == order_id) \
        .filter((Order.buyer_id == user_id) | (Order.seller_id == user_id)) \
        .all()

    if not row:
        flash(*order_not_found)
        return redirect(url_for('.get_orders'))

    order = {
        'id': row[0].Order.id,
        'amount': f'{row[0].Order.amount:,}',
        'recipient': row[0].Order.recipient,
        'cell_phone': row[0].Order.cell_phone,
        'address': row[0].Order.address,
        'insert_time': datetime.strftime(row[0].Order.insert_time, '%Y-%m-%d'),
        'update_time': datetime.strftime(row[0].Order.update_time, '%Y-%m-%d'),
        'order_status': row[0][2],
        'payment_status': row[0][3],
        'shipping_status': row[0][4],
        'order_items': []
    }
    for data in row:
        order['order_items'].append({
            'image_url': data.OrderItem.image_url,
            'name': data.OrderItem.name,
            'price': f'{data.OrderItem.price:,}',
            'quantity': data.OrderItem.quantity,
            'subtotal': f'{data.OrderItem.price * data.OrderItem.quantity:,}'
        })

    return render_template('orders/order.html', order=order)
