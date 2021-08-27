from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(140), nullable=False)
    cell_phone = db.Column(db.String(20))
    address = db.Column(db.String(100))
    store_introduction = db.Column(db.String(2000))
    role = db.Column(db.String(10), nullable=False, default='user')
    insert_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, nullable=False, default=datetime.now)

    cart = db.relationship('Cart', back_populates='user', uselist=False)
    for_sale = db.relationship('Product', back_populates='seller')
    delivery_orders = db.relationship('Order', back_populates='seller')
    purchase_order = db.relationship('Order', back_populates='buyer')
    rating_record = db.relationship('Rating', back_populates='rater')
    rated_record = db.relationship('Rating', back_populates='ratee')
    asked_questions = db.relationship('Question', back_populates='author')

    def __repr__(self):
        return f'<User {self.email}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
