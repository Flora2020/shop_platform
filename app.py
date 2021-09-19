import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from dotenv import load_dotenv

from middlewares import MethodRewriteMiddleware

if os.environ.get('FLASK_ENV', '') != 'production':
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
seeder = FlaskSeeder()
seeder.init_app(app, db)
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)


@app.route('/')
def home():
    products = Product.query.with_entities(Product.id, Product.name, Product.price, Product.image_url).filter(
        Product.inventory > 0).order_by(Product.insert_time.desc()).all()
    return render_template('home.html', products=products)


if __name__ == '__main__':
    from views import product_blueprint, user_blueprint, cart_blueprint
    from models import Product

    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(cart_blueprint, url_prefix='/carts')
    app.run()
