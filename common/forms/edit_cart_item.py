from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired, NumberRange


class EditCartItem(FlaskForm):
    quantity = IntegerField(
        u'數量',
        validators=[
            InputRequired(message=u'請輸入數量'),
            NumberRange(min=1, max=2147483647, message=u'數量須為 1 至 2147483647 間的整數')
        ]
    )