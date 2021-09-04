from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, NumberRange, URL

from models import Category
from common.forms.custom_validators import byte_length


categories = Category.query.with_entities(Category.id, Category.name).all()


class NewProduct(FlaskForm):
    name = StringField(u'商品名稱', validators=[InputRequired(), byte_length(max=60)])
    price = IntegerField(u'價格', validators=[InputRequired(), NumberRange(min=0, max=2147483647)])
    image = StringField(u'商品圖片網址', validators=[Optional(), URL(), byte_length(max=60)])
    inventory = IntegerField(u'庫存數量', validators=[InputRequired(), NumberRange(min=0, max=2147483647)])
    description = TextAreaField(u'商品描述', validators=[Optional(), byte_length(max=2000)])
    category = SelectField(u'分類', choices=[(category.id, category.name) for category in categories])
