from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, NumberRange, Regexp

from common.forms.custom_validators import byte_length


class NewOrder(FlaskForm):
    recipient = StringField(
        u'收件者姓名',
        validators=[
            InputRequired(message=u'請輸入收件者姓名'),
            byte_length(max=50, message=u'姓名須在 16 個中文字以內')
        ]
    )

    cell_phone = StringField(
        u'收件者手機號碼',
        validators=[
            InputRequired(message=u'請輸入手機號碼'),
            byte_length(max=20, message=u'手機號碼字數，須在 20 個字以內'),
            Regexp('^\+[0-9]{1,3}\.[0-9]{4,14}$', message=u'手機號碼格式須為 +國際碼.手機號碼。手機號碼需去掉最前方的 0')
        ]
    )

    address = StringField(
        u'收件地址',
        validators=[
            InputRequired(message=u'請輸入收件地址'),
            byte_length(max=100, message=u'收件地址字數，須在 33 個中文字以內')
        ]
    )
