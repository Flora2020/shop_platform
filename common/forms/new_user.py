from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, Optional, Regexp

from common.forms.custom_validators import byte_length


class NewUser(FlaskForm):
    display_name = StringField(
        u'*顯示名稱',
        validators=[
            InputRequired(message=u'請輸入顯示名稱'),
            byte_length(max=50, message=u'顯示名稱字數，須在 16 個中文字以內')
        ]
    )

    email = StringField(
        u'*電子信箱',
        validators=[
            InputRequired(message=u'請輸入電子信箱'),
            byte_length(max=50, message=u'電子信箱字數，須在 50 個英文字以內'),
            Email(message='信箱格式錯誤')
        ]
    )

    password = StringField(
        u'*密碼',
        validators=[
            InputRequired(message=u'請輸入密碼'),
            byte_length(max=50, message=u'密碼字數，須在 50 個字以內')
        ]
    )

    confirm_password = StringField(
        u'*確認密碼',
        validators=[
            InputRequired(message=u'請再次輸入密碼'),
            byte_length(max=50, message=u'確認密碼字數，須在 50 個字以內'),
            EqualTo('password', message=u'密碼與確認密碼不符')
        ]
    )

    cell_phone = StringField(
        u'手機號碼',
        validators=[
            Optional(),
            byte_length(max=20, message=u'手機號碼字數，須在 20 個字以內'),
            Regexp('^\+[0-9]{1,3}\.[0-9]{4,14}$', message=u'手機號碼格式須為 +國際碼.手機號碼。手機號碼需去掉最前方的 0')
        ]
    )

    address = StringField(
        u'寄件地址',
        validators=[
            Optional(),
            byte_length(max=100, message=u'寄件地址字數，須在 33 個中文字以內')
        ]
    )

    store_introduction = TextAreaField(
        u'商家描述',
        validators=[
            Optional(),
            byte_length(max=2000, message=u'商家描述字數，須在 666 個中文字以內')
        ]
    )
