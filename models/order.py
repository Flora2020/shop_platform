from app import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    recipient = db.Column(db.String(50), nullable=False)
    cell_phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    insert_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, nullable=False, default=datetime.now)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shopping_status_id = db.Column(db.Integer, db.ForeignKey('shopping_status.id'))
    payment_status_id = db.Column(db.Integer, db.ForeignKey('payment_status.id'))

    seller = db.relationship('User', back_populates='delivery_orders')
    buyer = db.relationship('User', back_populates='purchase_order')
    shopping_status = db.relationship('ShoppingStatus', back_populates='orders')
    payment_status = db.relationship('PaymentStatus', back_populates='orders')
    payments = db.relationship('Payment', back_populates='order')

    def __repr__(self):
        return f'<Order {self.id}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
