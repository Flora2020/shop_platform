from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
seeder = FlaskSeeder()
mail = Mail()
