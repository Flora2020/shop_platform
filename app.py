import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder


if os.environ.get('FLASK_ENV', '') != 'production':
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
seeder = FlaskSeeder()
seeder.init_app(app, db)


@app.route('/')
def home():
    products = Product.query.with_entities(Product.name, Product.price, Product.image_url).order_by(
        Product.insert_time.desc()).all()
    return render_template('home.html', products=products)


if __name__ == '__main__':
    from views import product_blueprint
    from models import Product
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.run()
