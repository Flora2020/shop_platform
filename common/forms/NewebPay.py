from flask_wtf import FlaskForm
from wtforms import StringField


class NewebPayForm(FlaskForm):
    # 藍新金流Newebpay_MPG串接手冊_MPG_1.1.1 page 33-34
    MerchantID = StringField()
    TradeInfo = StringField()
    TradeSha = StringField()
    Version = StringField()
