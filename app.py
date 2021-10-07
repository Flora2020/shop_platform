import os

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_mail import Mail
from dotenv import load_dotenv

if os.environ.get('FLASK_ENV', '') != 'production':
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
seeder = FlaskSeeder()
seeder.init_app(app, db)
mail = Mail(app)


@app.route('/')
def home():
    return redirect(url_for('products.get_products'))


if __name__ == '__main__':
    from views import product_blueprint, user_blueprint, cart_blueprint, order_blueprint

    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(cart_blueprint, url_prefix='/carts')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.run(port=os.environ.get('PORT'))
