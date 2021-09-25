from app import db
from datetime import datetime


class ShippingStatus(db.Model):
    __tablename__ = 'shipping_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(60), unique=True, nullable=False)
    insert_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, nullable=False, default=datetime.now)
    orders = db.relationship('Order', back_populates='shipping_status')

    def __repr__(self):
        return f'<ShippingStatus {self.status}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
