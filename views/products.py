from functools import partial
from flask import Blueprint, redirect, url_for, request, render_template, flash, session

from models import Product, Category
from models.user.decorators import require_login
from common.utils import pretty_date
from common.flash_message import product_not_found, seller_products_not_found, product_update_success
from common.generate_many_flash_message import generate_many_flash_message
from common.forms import NewProduct

product_blueprint = Blueprint('products', __name__)


@product_blueprint.route('/')
def get_products():
    return redirect(url_for('home'))


@product_blueprint.route('/<string:product_id>', methods=['GET'])
def get_product(product_id):
    if request.method == 'GET':
        if not product_id.isnumeric():
            flash(*product_not_found)
            return redirect(url_for('home'))

        product = Product.find_by_id(product_id)
        if product:
            product.update_time = pretty_date(product.update_time)

            user_id = None
            if session.get('user') and session['user'].get('id'):
                user_id = session['user']['id']

            return render_template('/products/product.html', product=product, user_id=user_id)
        else:
            flash(*product_not_found)
            return redirect(url_for('home'))


@product_blueprint.route('/seller/<string:seller_id>')
def get_seller_products(seller_id):
    if not seller_id.isnumeric():
        flash(*seller_products_not_found)
        return redirect(url_for('home'))

    products = Product.query\
        .with_entities(Product.id, Product.name, Product.price, Product.image_url, Product.seller_id)\
        .filter(Product.seller_id == seller_id, Product.inventory > 0)\
        .order_by(Product.insert_time.desc()).all()

    if products:
        user_id = None
        if session.get('user') and session['user'].get('id'):
            user_id = session['user']['id']

        return render_template('home.html', products=products, user_id=user_id)
    else:
        flash(*seller_products_not_found)
        return redirect(url_for('home'))


@product_blueprint.route('/new', methods=['GET', 'POST'])
@require_login
def new_product():
    form = NewProduct()
    categories = Category.query.with_entities(Category.id, Category.name).all()
    form.category.choices = [(category.id, category.name) for category in categories]
    if form.validate_on_submit():
        seller_id = session['user']['id']
        product = Product(name=form.name.data,
                          price=form.price.data,
                          image_url=form.image.data,
                          inventory=form.inventory.data,
                          description=form.description.data,
                          seller_id=seller_id,
                          category_id=form.category.data)
        product.save_to_db()
        return redirect(url_for('products.get_seller_products', seller_id=seller_id))
    else:
        flash_warning_messages = partial(generate_many_flash_message, category='warning')
        flash_warning_messages(form.name.errors)
        flash_warning_messages(form.price.errors)
        flash_warning_messages(form.image.errors)
        flash_warning_messages(form.inventory.errors)
        flash_warning_messages(form.description.errors)
        if form.category.errors:
            flash_warning_messages(['查無此分類'])

    is_new_product = True
    return render_template('products/new.html', form=form, is_new_product=is_new_product)


@product_blueprint.route('/edit/<string:product_id>', methods=['GET', 'POST'])
@require_login
def edit_product(product_id):
    if not product_id.isnumeric():
        flash(*product_not_found)
        return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

    product = Product.find_by_id(product_id)
    form = NewProduct()
    categories = Category.query.with_entities(Category.id, Category.name).all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if request.method == 'GET':
        if not product:
            flash(*product_not_found)
            return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

        if product.seller_id != session['user']['id']:
            flash(*product_not_found)
            return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

        form.name.data = product.name
        form.price.data = product.price
        form.image.data = product.image_url
        form.inventory.data = product.inventory
        form.description.data = product.description
        form.category.data = product.category.id

    if request.method == 'POST':
        if form.validate_on_submit():
            product.name = form.name.data
            product.price = form.price.data
            product.image_url = form.image.data
            product.inventory = form.inventory.data
            product.description = form.description.data
            product.category = Category.find_by_id(form.category.data)

            product.save_to_db()
            flash(*product_update_success)
            return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

        else:
            flash_warning_messages = partial(generate_many_flash_message, category='warning')
            flash_warning_messages(form.name.errors)
            flash_warning_messages(form.price.errors)
            flash_warning_messages(form.image.errors)
            flash_warning_messages(form.inventory.errors)
            flash_warning_messages(form.description.errors)
            if form.category.errors:
                flash_warning_messages(['查無此分類'])

    is_new_product = False
    return render_template('products/new.html', form=form, is_new_product=is_new_product, product_id=product.id)


@product_blueprint.route('/delete/<string:product_id>', methods=['POST'])
@require_login
def delete_product(product_id):
    if not product_id.isnumeric():
        flash(*product_not_found)
        return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

    product = Product.find_by_id(product_id)

    if product.seller_id != session['user']['id']:
        flash(*product_not_found)
        return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

    product.delete()
    return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))


