import os
from dotenv import load_dotenv

if os.environ.get('FLASK_ENV', '') != 'production':
    load_dotenv()  # aes_encrypt needs environ variables


def test_aes_encrypt():
    from helpers.orders_view_helper.get_payment_data import aes_encrypt

    # 藍新金流Newebpay_MPG串接手冊_MPG_1.1.1 page 65-66 範例資料
    data = 'MerchantID=3430112&RespondType=JSON&TimeStamp=1485232229&Version=1.4&MerchantOrderNo=S_1485232229&Amt=40&ItemDesc=UnitTest'
    Key = '12345678901234567890123456789012'.encode('ascii')
    IV = '1234567890123456'.encode('ascii')
    expect_output = 'ff91c8aa01379e4de621a44e5f11f72e4d25bdb1a18242db6cef9ef07d80b0165e476fd1d9acaa53170272c82d122961e1a0700a7427cfa1cf90db7f6d6593bbc93102a4d4b9b66d9974c13c31a7ab4bba1d4e0790f0cbbbd7ad64c6d3c8012a601ceaa808bff70f94a8efa5a4f984b9d41304ffd879612177c622f75f4214fa'

    assert aes_encrypt(data, Key, IV) == expect_output
