from flask import Blueprint, redirect, url_for


product_blueprint = Blueprint('products', __name__)


@product_blueprint.route('/')
def get_products():
    return redirect(url_for('home'))

