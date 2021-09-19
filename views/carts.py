from datetime import datetime
from flask import Blueprint, session, redirect, flash, render_template, url_for, request

from models import Product, Cart, CartItem
from common.previous_page import previous_page
from common.utils import find_one_dictionary_in_list
from common.flash_message import product_not_found, cart_is_empty
from common.constant import USER, CART_ID, CART_ITEMS, PRODUCT_ID, QUANTITY, INSERT_TIME, UPDATE_TIME
from common.forms import EditCartItem

cart_blueprint = Blueprint('carts', __name__)


@cart_blueprint.route('/')
def get_cart_items():
    cart_items = None
    form = EditCartItem()

    if session.get(USER) and session.get(USER).get(CART_ID):
        cart_items = CartItem.query\
            .with_entities(CartItem.product_id, CartItem.quantity,  Product.name, Product.price, Product.image_url)\
            .join(Product)\
            .filter(CartItem.cart_id == session.get(USER).get(CART_ID))\
            .filter(CartItem.product_id == Product.id).all()

    elif session.get(CART_ITEMS):
        for item in session[CART_ITEMS]:
            product = Product.query\
                .with_entities(Product.name, Product.price, Product.image_url)\
                .filter(Product.id == item[PRODUCT_ID])\
                .first()
            item['name'] = product.name
            item['price'] = product.price
            item['image_url'] = product.image_url
        cart_items = session[CART_ITEMS]

    if not cart_items:
        flash(*cart_is_empty)
        return redirect(url_for('home'))

    return render_template('carts/cart_items.html', cart_items=cart_items, form=form)


@cart_blueprint.route('/<string:product_id>', methods=['POST'])
def new_cart(product_id):
    if not product_id.isnumeric() or not Product.find_by_id(product_id):
        flash(*product_not_found)
        return redirect(previous_page())

    cart_id = session.get(USER) and session[USER].get(CART_ID)
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


@cart_blueprint.route('/edit/<string:product_id>', methods=['POST'])
def edit_cart_item(product_id):
    return 'data received'
