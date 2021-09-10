from functools import partial
from flask import Blueprint, redirect, url_for, request, render_template, flash, session

from models import Product
from models.user.decorators import require_login
from common.utils import pretty_date
from common.flash_message import product_not_found, seller_products_not_found
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
            return render_template('/products/product.html', product=product)
        else:
            flash(*product_not_found)
            return redirect(url_for('home'))


@product_blueprint.route('/seller/<string:seller_id>')
def get_seller_products(seller_id):
    if not seller_id.isnumeric():
        flash(*seller_products_not_found)
        return redirect(url_for('home'))

    products = Product.query.with_entities(Product.id, Product.name, Product.price, Product.image_url).filter(
        Product.seller_id == seller_id, Product.inventory > 0).order_by(Product.insert_time.desc()).all()
    if products:
        return render_template('home.html', products=products)
    else:
        flash(*seller_products_not_found)
        return redirect(url_for('home'))


@product_blueprint.route('/new', methods=['GET', 'POST'])
@require_login
def new_product():
    form = NewProduct()
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

    return render_template('products/new.html', form=form)
