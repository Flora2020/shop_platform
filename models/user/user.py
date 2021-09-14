from datetime import datetime
from typing import Dict
from passlib.hash import pbkdf2_sha256
from flask import session

from app import db
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from models.user.errors import EmailAlreadyUsedError, DisplayNameAlreadyUsedError, InvalidLoginError


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
    delivery_orders = db.relationship('Order', primaryjoin='Order.seller_id == User.id', back_populates='seller')
    purchase_order = db.relationship('Order', primaryjoin='Order.buyer_id == User.id', back_populates='buyer')
    rating_record = db.relationship('Rating', primaryjoin='Rating.rater_id == User.id', back_populates='rater')
    rated_record = db.relationship('Rating', primaryjoin='Rating.ratee_id == User.id', back_populates='ratee')
    asked_questions = db.relationship('Question', back_populates='author')
    replies = db.relationship('Reply', back_populates='author')

    def __repr__(self):
        return f'<User {self.email}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self) -> Dict:
        return {
            'id': self.id,
            'display_name': self.display_name,
            'email': self.email,
            'cell_phone': self.cell_phone,
            'address': self.address,
            'store_introduction': self.store_introduction,
            'role': self.role,
            'cart_id': self.cart.id
        }

    def find_or_create_cart(self) -> 'Cart':
        if not self.cart:
            cart = Cart(user_id=self.id)
            cart.save_to_db()

        if not session.get('cartitems'):
            return self.cart

        cart_id = self.cart.id
        for item in session.get('cartitems'):
            if not Product.find_by_id(item['product_id']):
                continue

            CartItem(
                cart_id=cart_id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                insert_time=item['insert_time'],
                update_time=item['update_time']
            ).save_to_db()

        session['cartitems'] = None
        return self.cart

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_display_name(cls, display_name):
        return cls.query.filter_by(display_name=display_name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def register(cls, display_name: str, email: str, password: str, cell_phone: str = None, address: str = None,
                 store_introduction: str = None) -> bool:

        if cls.find_by_email(email):
            raise EmailAlreadyUsedError('此信箱已註冊，請更換信箱')

        if cls.find_by_display_name(display_name):
            raise DisplayNameAlreadyUsedError('此顯示名稱已有人使用，請更換顯示名稱')

        hash_password = pbkdf2_sha256.hash(password)
        cls(
            display_name=display_name,
            email=email,
            password=hash_password,
            cell_phone=cell_phone,
            address=address,
            store_introduction=store_introduction
        ).save_to_db()

        return True

    @classmethod
    def login(cls, display_name: str, password: str) -> 'User':
        user = cls.find_by_display_name(display_name)

        if not user:
            raise InvalidLoginError('顯示名稱或密碼錯誤')

        if not pbkdf2_sha256.verify(password, user.password):
            raise InvalidLoginError('顯示名稱或密碼錯誤')

        return user
