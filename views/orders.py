from functools import partial
from flask import Blueprint, render_template, session, redirect, url_for, flash, request

from common.forms import NewOrder
from models import CartItem, Product, Order, OrderItem
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
        OrderItem(order_id=order.id, product_id=item.product_id, price=item.product.price, quantity=item.quantity) \
            .save_to_db()
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
        .with_entities(OrderItem.price, OrderItem.quantity, Product.image_url, Product.name) \
        .join(Product) \
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
            return redirect(url_for('home'))

        else:
            flash_warning_messages(form.recipient.errors)
            flash_warning_messages(form.cell_phone.errors)
            flash_warning_messages(form.address.errors)

    return render_template('orders/new.html', form=form, order_id=order_id, order_items=order_items, amount=amount)
