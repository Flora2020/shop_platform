from app import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(100))
    inventory = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2000))
    insert_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, nullable=False, default=datetime.now)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    seller = db.relationship('User', back_populates='for_sale')
    category = db.relationship('Category', back_populates='products')
    carts = db.relationship('CartItem', back_populates='product')
    orders = db.relationship('OrderItem', back_populates='product')
    questions = db.relationship('Question', back_populates='product')

    def __repr__(self):
        return f'<Product id: {self.id}, name: {self.name}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
