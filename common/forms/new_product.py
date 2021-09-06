from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, NumberRange, URL

from models import Category
from common.forms.custom_validators import byte_length


categories = Category.query.with_entities(Category.id, Category.name).all()


class NewProduct(FlaskForm):
    name = StringField(
        u'商品名稱',
        validators=[
            InputRequired(message=u'請輸入商品名稱'),
            byte_length(max=60, message=u'商品名稱字數，須在 20 個中文字以內')
        ]
    )

    price = IntegerField(
        u'價格',
        validators=[
            InputRequired(message=u'請輸入價格'),
            NumberRange(min=0, max=2147483647, message=u'價格須為 0 至 2147483647 間的整數')
        ]
    )

    image = StringField(
        u'商品圖片網址',
        validators=[
            Optional(),
            URL(message=u'圖片網址格式錯誤'),
            byte_length(max=100, message=u'圖片網址字數，須在 100 個英文字以內')
        ]
    )

    inventory = IntegerField(
        u'庫存數量',
        validators=[
            InputRequired(message=u'請輸入庫存數量'),
            NumberRange(min=0, max=2147483647, message=u'庫存數量須為 0 至 2147483647 間的整數')
        ]
    )

    description = TextAreaField(
        u'商品描述',
        validators=[
            Optional(),
            byte_length(max=2000, message=u'商品描述字數，須在 666 個中文字以內')
        ]
    )

    category = SelectField(
        u'分類',
        choices=[(category.id, category.name) for category in categories],
        validate_choice=True
    )
