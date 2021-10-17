from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, NumberRange

from common.forms.custom_validators import byte_length


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

    image = FileField(
        u'商品圖片',
        validators=[
            FileAllowed(upload_set=['jpg', 'jpge', 'png', 'gif'], message=u'只接受 .jpg、.jpge、.png、.gif 檔案'),
            FileSize(max_size=1048576, message=u'圖片大小需小於 1 MB')
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
        coerce=int,
        validate_choice=True
    )
