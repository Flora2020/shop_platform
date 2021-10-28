from helpers.orders_view_helper.get_payment_data import get_trade_sha

# 藍新金流Newebpay_MPG串接手冊_MPG_1.1.1 page 70 範例程式

trade_info = 'ff91c8aa01379e4de621a44e5f11f72e4d25bdb1a18242db6cef9ef07d80b0165e476fd1d9acaa53170272c82d122961e1a0700a7427cfa1cf90db7f6d6593bbc93102a4d4b9b66d9974c13c31a7ab4bba1d4e0790f0cbbbd7ad64c6d3c8012a601ceaa808bff70f94a8efa5a4f984b9d41304ffd879612177c622f75f4214fa'
key = '12345678901234567890123456789012'
iv = '1234567890123456'
expect_output = 'EA0A6CC37F40C1EA5692E7CBB8AE097653DF3E91365E6A9CD7E91312413C7BB8'
result = get_trade_sha(trade_info, key, iv)

if result != expect_output:
    print('not pass')
else:
    print('pass')
