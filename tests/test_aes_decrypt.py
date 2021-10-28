from dotenv import load_dotenv
load_dotenv()  # aes_decrypt needs environ variables


def test_aes_decrypt():
    from helpers.orders_view_helper import aes_decrypt

    # 藍新金流Newebpay_MPG串接手冊_MPG_1.1.1 page 65-66 範例資料
    data = 'ff91c8aa01379e4de621a44e5f11f72e4d25bdb1a18242db6cef9ef07d80b0165e476fd1d9acaa53170272c82d122961e1a0700a7427cfa1cf90db7f6d6593bbc93102a4d4b9b66d9974c13c31a7ab4bba1d4e0790f0cbbbd7ad64c6d3c8012a601ceaa808bff70f94a8efa5a4f984b9d41304ffd879612177c622f75f4214fa'
    key = '12345678901234567890123456789012'.encode('ascii')
    iv = '1234567890123456'.encode('ascii')
    expect_output = 'MerchantID=3430112&RespondType=JSON&TimeStamp=1485232229&Version=1.4&MerchantOrderNo=S_1485232229&Amt=40&ItemDesc=UnitTest'

    assert aes_decrypt(data, key, iv) == expect_output
