from app import db
from datetime import datetime


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer,  nullable=False)
    insert_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, nullable=False, default=datetime.now)

    order = db.relationship('Order', back_populates='products')
    product = db.relationship('Product', back_populates='orders')
    rating = db.relationship('Rating', back_populates='order_item', uselist=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_order_id(cls, order_id):
        return cls.query.filter_by(order_id=order_id).first()

    @classmethod
    def find_by_product_id(cls, product_id):
        return cls.query.filter_by(product_id=product_id).first()
