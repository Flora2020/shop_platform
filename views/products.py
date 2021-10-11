from functools import partial
from flask import Blueprint, redirect, url_for, request, render_template, flash, session
from sqlalchemy import and_, desc, asc

from models import Product, Category
from models.user.decorators import require_login
from common.utils import pretty_date
from common.flash_message import product_not_found, seller_products_not_found, product_update_success
from common.generate_many_flash_message import generate_many_flash_message
from common.forms import NewProduct

product_blueprint = Blueprint('products', __name__)
products_per_page = 20
product_order_select_options = {
    'sorting_field': [('insert_time', u'上架日期'), ('price', '單價')],
    'order': [('desc', 'Z→A'), ('asc', 'A→Z')]
}
sorting_field_default = product_order_select_options['sorting_field'][0][0]
order_default = product_order_select_options['order'][0][0]
sorting_field_to_model_col = {
    'insert_time': Product.insert_time,
    'price': Product.price
}


@product_blueprint.route('/')
def get_products():
    page = request.args.get('page')
    keyword = request.args.get('keyword', '').strip()
    category_id = request.args.get('category_id', '')
    sorting_field = request.args.get('sorting_field', sorting_field_default)
    order = request.args.get('order', order_default)

    categories = Category.query.with_entities(Category.id, Category.name).all()
    filter_conditions = []
    sort_conditions = []

    if not page or not page.isnumeric():
        page = 1
    else:
        page = int(page) or 1

    if keyword:
        filter_conditions.append(Product.name.like(f'%{keyword}%'))
    if category_id and category_id.isnumeric():
        category_id = int(category_id)
        filter_conditions.append(Product.category_id == category_id)
    if order == 'desc':
        sort_conditions.append(desc(sorting_field_to_model_col.get(sorting_field, Product.insert_time)))
    else:
        sort_conditions.append(asc(sorting_field_to_model_col.get(sorting_field, Product.price)))

    pagination = Product.query \
        .with_entities(Product.id, Product.name, Product.price, Product.image_url, Product.seller_id) \
        .filter(Product.inventory > 0) \
        .filter(and_(*filter_conditions)) \
        .order_by(*sort_conditions) \
        .paginate(page=page, per_page=products_per_page, error_out=False, max_per_page=None)

    products = pagination.items
    if not products and page != 1:
        return redirect(url_for('.get_products', page=pagination.pages))

    user_id = None
    if session.get('user') and session['user'].get('id'):
        user_id = session['user']['id']

    return render_template('products/products.html',
                           products=products,
                           user_id=user_id,
                           paginate=pagination,
                           endpoint='products.get_products',
                           categories=categories,
                           order_options=product_order_select_options,
                           selected_options={
                               'keyword': keyword,
                               'category_id': category_id,
                               'sorting_field': sorting_field,
                               'order': order
                           })


@product_blueprint.route('/<string:product_id>', methods=['GET'])
def get_product(product_id):
    if request.method == 'GET':
        product = Product.find_by_id(product_id)
        if product:
            product.update_time = pretty_date(product.update_time)

            user_id = None
            if session.get('user') and session['user'].get('id'):
                user_id = session['user']['id']

            return render_template('/products/product.html', product=product, user_id=user_id)
        else:
            flash(*product_not_found)
            return redirect(url_for('.get_products'))


@product_blueprint.route('/seller/<string:seller_id>')
def get_seller_products(seller_id):
    page = request.args.get('page')
    keyword = request.args.get('keyword', '').strip()
    category_id = request.args.get('category_id', '')
    sorting_field = request.args.get('sorting_field', sorting_field_default)
    order = request.args.get('order', order_default)

    categories = Category.query.with_entities(Category.id, Category.name).all()
    filter_conditions = []
    sort_conditions = []

    if not page or not page.isnumeric():
        page = 1
    else:
        page = int(page) or 1

    if not seller_id.isnumeric():
        flash(*seller_products_not_found)
        return redirect(url_for('.get_products'))

    if keyword:
        filter_conditions.append(Product.name.like(f'%{keyword}%'))
    if category_id and category_id.isnumeric():
        category_id = int(category_id)
        filter_conditions.append(Product.category_id == category_id)
    if order == 'desc':
        sort_conditions.append(desc(sorting_field_to_model_col.get(sorting_field, Product.insert_time)))
    else:
        sort_conditions.append(asc(sorting_field_to_model_col.get(sorting_field, Product.price)))

    pagination = Product.query \
        .with_entities(Product.id, Product.name, Product.price, Product.image_url, Product.seller_id) \
        .filter(Product.seller_id == seller_id, Product.inventory > 0) \
        .filter(and_(*filter_conditions)) \
        .order_by(*sort_conditions) \
        .paginate(page=page, per_page=products_per_page, error_out=False, max_per_page=None)

    products = pagination.items
    if not products and page != 1:
        return redirect(url_for('.get_seller_products', seller_id=seller_id, page=pagination.pages))

    user_id = None
    if session.get('user') and session['user'].get('id'):
        user_id = session['user']['id']

    return render_template('products/products.html',
                           products=products,
                           user_id=user_id,
                           paginate=pagination,
                           endpoint='products.get_seller_products',
                           seller_id=seller_id,
                           categories=categories,
                           order_options=product_order_select_options,
                           selected_options={
                               'keyword': keyword,
                               'category_id': category_id,
                               'sorting_field': sorting_field,
                               'order': order
                           })


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
    product = Product.find_by_id(product_id)
    if not product:
        flash(*product_not_found)
        return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

    if product.seller_id != session['user']['id']:
        flash(*product_not_found)
        return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

    form = NewProduct()
    categories = Category.query.with_entities(Category.id, Category.name).all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if request.method == 'GET':
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
    product = Product.find_by_id(product_id)
    if not product:
        flash(*product_not_found)
        return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

    if product.seller_id != session['user']['id']:
        flash(*product_not_found)
        return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))

    product.delete()
    return redirect(url_for('products.get_seller_products', seller_id=session['user']['id']))
