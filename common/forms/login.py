from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

from common.forms.custom_validators import byte_length


class Login(FlaskForm):
    display_name = StringField(
        u'*顯示名稱',
        validators=[
            InputRequired(message=u'請輸入顯示名稱'),
            byte_length(max=50, message=u'顯示名稱字數，須在 16 個中文字以內')
        ]
    )

    password = StringField(
        u'*密碼',
        validators=[
            InputRequired(message=u'請輸入密碼'),
            byte_length(max=50, message=u'密碼字數，須在 50 個字以內')
        ]
    )