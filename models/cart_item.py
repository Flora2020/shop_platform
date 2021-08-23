from app import db
from datetime import datetime


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    insert_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, nullable=False, default=datetime.now)
    cart = db.relationship('Cart', back_populates='products')
    product = db.relationship('Product', back_populates='carts')

    def __repr__(self):
        return f'<CartItem cart_id: {self.cart_id}, product_id: {self.product_id}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_cart_id(cls, cart_id):
        return cls.query.filter_by(cart_id=cart_id).all()

    @classmethod
    def find_by_product_id(cls, product_id):
        return cls.query.filter_by(product_id=product_id).all()
