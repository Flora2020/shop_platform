from app import db
from datetime import datetime


class Rating(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.SmallInteger, nullable=False)
    comment = db.Column(db.String(2000))
    insert_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, nullable=False, default=datetime.now)
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ratee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_item_order_id = db.Column(db.Integer, nullable=False)
    order_item_product_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['order_item_order_id', 'order_item_product_id'],
            ['order_item.order_id', 'order_item.product_id']
        ),
    )

    rater = db.relationship('User', back_populates="rating_record")
    ratee = db.relationship('User', back_populates="rated_record")
    order_item = db.relationship('OrderItem', back_populates="rating")

    def __repr__(self):
        return f'<Rating score: {self.score}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
