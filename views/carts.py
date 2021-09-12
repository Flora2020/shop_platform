from datetime import datetime
from flask import Blueprint, session, redirect, flash

from models import Product, Cart, CartItem
from common.previous_page import previous_page
from common.utils import find_one_dictionary_in_list
from common.flash_message import product_not_found

cart_blueprint = Blueprint('carts', __name__)

# dictionary keys
CART_ITEMS = 'cartitems'
PRODUCT_ID = 'product_id'
QUANTITY = 'quantity'
INSERT_TIME = 'insert_time'
UPDATE_TIME = 'update_time'


@cart_blueprint.route('/<string:product_id>', methods=['POST'])
def new_cart(product_id):
    if not product_id.isnumeric() or not Product.find_by_id(product_id):
        flash(*product_not_found)
        return redirect(previous_page())

    cart_id = session.get('user') and session['user'].get('cart_id')
    if cart_id is None:
        # save cart items to session
        # cart item format: {'product_id': int, 'quantity': int, 'insert_time': datetime , 'update_time': datetime}
        cart_items = session.get(CART_ITEMS, [])
        item = find_one_dictionary_in_list(cart_items, PRODUCT_ID, product_id)
        if item is None:
            cart_items.append({
                PRODUCT_ID: product_id,
                QUANTITY: 1,
                INSERT_TIME: datetime.now(),
                UPDATE_TIME: datetime.now()
            })
        else:
            item[QUANTITY] = item.get(QUANTITY, 0) + 1
            item[UPDATE_TIME] = datetime.now()

        session[CART_ITEMS] = cart_items

    else:
        # save cart items to database
        cart = Cart.find_by_id(cart_id)
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item is None:
            CartItem(cart_id=cart.id, product_id=product_id, quantity=1).save_to_db()
        else:
            cart_item.quantity += 1
            cart_item.save_to_db()

    return redirect(previous_page())
