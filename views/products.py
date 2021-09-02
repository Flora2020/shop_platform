from flask import Blueprint, redirect, url_for, request, render_template, flash
from models import Product
from common.utils import pretty_date
from common.flash_message import product_not_found


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
