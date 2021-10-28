import os
from dotenv import load_dotenv

if os.environ.get('FLASK_ENV', '') != 'production':
    load_dotenv()  # get_payment_data.py needs environ variables


def test_query_string_encode():
    from helpers.orders_view_helper.get_payment_data import query_string_encode

    data = {
        'MerchantID': 3430112,
        'RespondType': 'JSON',
        'TimeStamp': 1485232229,
        'Version': 1.4,
        'MerchantOrderNo': 'S_1485232229',
        'Amt': 40,
        'ItemDesc': 'UnitTest'
    }
    expect_output = 'MerchantID=3430112&RespondType=JSON&TimeStamp=1485232229&Version=1.4&MerchantOrderNo=S_1485232229&Amt=40&ItemDesc=UnitTest'

    assert query_string_encode(data) == expect_output
