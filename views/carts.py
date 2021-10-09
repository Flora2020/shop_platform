from datetime import datetime
from functools import partial
from flask import Blueprint, session, redirect, flash, render_template, url_for

from models import Product, Cart, CartItem, User
from common.previous_page import previous_page
from common.utils import find_one_dictionary_in_list
from common.generate_many_flash_message import generate_many_flash_message
from common.flash_message import product_not_found, cart_is_empty
from common.constant import USER, CART_ID, CART_ITEMS, PRODUCT_ID, QUANTITY, INSERT_TIME, UPDATE_TIME
from common.forms import EditCartItem

cart_blueprint = Blueprint('carts', __name__)


@cart_blueprint.route('/')
def get_cart_items():
    cart_items = None
    sellers = set()
    total = 0
    form = EditCartItem()

    if session.get(USER) and session.get(USER).get(CART_ID):
        row = CartItem.query \
            .with_entities(CartItem.product_id, CartItem.quantity, Product.name,
                           Product.price, Product.image_url, Product.seller_id) \
            .join(Product) \
            .filter(CartItem.cart_id == session.get(USER).get(CART_ID)) \
            .filter(CartItem.product_id == Product.id) \
            .order_by(Product.seller_id.asc()) \
            .all()

        cart_items = []
        for data in row:
            subtotal = data['price'] * data[QUANTITY]
            total += subtotal
            seller_name = User.query.with_entities(User.display_name).filter(User.id == data.seller_id).first()
            sellers.add((data['seller_id'], seller_name[0]))
            item = {
                PRODUCT_ID: data[PRODUCT_ID],
                QUANTITY: data[QUANTITY],
                'name': data['name'],
                'price': f'{data["price"]:,}',
                'image_url': data['image_url'],
                'subtotal': f'{subtotal:,}',
                'seller_id': data['seller_id'],
                'seller_name': seller_name[0]
            }
            cart_items.append(item)

    elif session.get(CART_ITEMS):
        for item in session[CART_ITEMS]:
            product = Product.query \
                .with_entities(Product.name, Product.price, Product.image_url, Product.seller_id, User.display_name) \
                .join(User) \
                .filter(Product.id == item[PRODUCT_ID]) \
                .first()

            subtotal = product.price * item[QUANTITY]
            total += subtotal
            sellers.add((product.seller_id, product.display_name))

            item['name'] = product.name
            item['price'] = f'{product.price:,}'
            item['subtotal'] = f'{subtotal:,}'
            item['image_url'] = product.image_url
            item['seller_id'] = product.seller_id
            item['seller_name'] = product.display_name

        session[CART_ITEMS].sort(key=lambda item: item['seller_id'])
        cart_items = session[CART_ITEMS]

    if not cart_items:
        flash(*cart_is_empty)
        return redirect(url_for('home'))

    total = f'{total:,}'
    return render_template('carts/cart_items.html', cart_items=cart_items, form=form, total=total, sellers=sellers)


@cart_blueprint.route('/<string:product_id>', methods=['POST'])
def new_cart(product_id):
    if not Product.find_by_id(product_id):
        flash(*product_not_found)
        return redirect(previous_page())

    cart_id = session.get(USER) and session[USER].get(CART_ID)
    if cart_id is None:
        # save cart items to session
        # cart item format: {'product_id': int, 'quantity': int, 'insert_time': datetime , 'update_time': datetime}
        cart_items = session.get(CART_ITEMS, [])
        result = find_one_dictionary_in_list(cart_items, PRODUCT_ID, product_id)

        if result is None:
            cart_items.append({
                PRODUCT_ID: product_id,
                QUANTITY: 1,
                INSERT_TIME: datetime.now(),
                UPDATE_TIME: datetime.now()
            })
        else:
            _, item = result
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
    if not Product.find_by_id(product_id):
        flash(*product_not_found)
        return redirect(previous_page())

    form = EditCartItem()
    if form.validate_on_submit():
        cart_id = session.get(USER) and session[USER].get(CART_ID)

        if cart_id:
            cart_item = CartItem.find_by_composite_primary_key(cart_id=cart_id, product_id=product_id)
            if not cart_item:
                flash(*product_not_found)
                return redirect(previous_page())

            cart_item.quantity = form.quantity.data
            cart_item.save_to_db()

        else:
            result = find_one_dictionary_in_list(session[CART_ITEMS], PRODUCT_ID, product_id)
            if result is None:
                flash(*product_not_found)
                return redirect(previous_page())

            _, cart_item = result
            cart_item[QUANTITY] = form.quantity.data
            session.modified = True

    else:
        flash_warning_messages = partial(generate_many_flash_message, category='warning')
        flash_warning_messages(form.quantity.errors)

    return redirect(url_for('carts.get_cart_items'))


@cart_blueprint.route('/delete/<string:product_id>', methods=['POST'])
def delete_cart_item(product_id):
    if not Product.find_by_id(product_id):
        flash(*product_not_found)
        return redirect(url_for('carts.get_cart_items'))

    if session.get(USER) and session.get(USER).get(CART_ID):
        cart_item = CartItem.find_by_composite_primary_key(
            cart_id=session[USER][CART_ID],
            product_id=product_id
        )

        if not cart_item:
            flash(*product_not_found)
            return redirect(url_for('carts.get_cart_items'))

        cart_item.delete()

    elif session.get(CART_ITEMS):
        item = find_one_dictionary_in_list(session[CART_ITEMS], PRODUCT_ID, product_id)

        if item is None:
            flash(*product_not_found)
            return redirect(url_for('carts.get_cart_items'))

        del session[CART_ITEMS][item[0]]
        session.modified = True

    else:
        flash(*product_not_found)

    return redirect(url_for('carts.get_cart_items'))
