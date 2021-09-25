from flask import Blueprint, render_template, session, redirect, url_for, flash

from common.forms import NewOrder
from models import CartItem, Product, Order, OrderItem
from models.user.decorators import require_login
from common.constant import USER, CART_ID
from common.flash_message import product_not_found

order_blueprint = Blueprint('orders', __name__)


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
        shipping_status_id=1,
        payment_status_id=1,
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
    order = Order.find_by_id(order_id)
    form = NewOrder()
    form.amount.data = order.amount
    form.recipient.data = order.recipient
    form.cell_phone.data = order.cell_phone if order.cell_phone != 'None' else None
    form.address.data = order.address if order.address != 'None' else None
    return render_template('orders/new.html', form=form, order_id=order_id)
