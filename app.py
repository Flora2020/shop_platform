import os
from flask import Flask
from common.database import db
from dotenv import load_dotenv

if os.environ.get('FLASK_ENV', '') != 'production':
    load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')


@app.route('/')
def home():
    return 'Hello World!'


if __name__ == '__main__':
    db.init_app(app)
    app.run()
