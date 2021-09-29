import os
from datetime import datetime
from typing import Dict, Union

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

HashKey = os.environ.get('HashKey')
HashIV = os.environ.get('HashIV')
URL = os.environ.get('URL')


def query_string_encode(data: Dict) -> str:
    key_value_pairs = []
    for key, value in data.items():
        key_value_pairs.append(f'{key}={value}')

    return '&'.join(key_value_pairs)


def aes_encrypt(data: str, key: bytes = HashKey.encode('ascii'), iv: bytes = HashIV.encode('ascii')) -> str:
    # 藍新金流Newebpay_MPG串接手冊_MPG_1.1.1 page 65
    # aes-256-cbc
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphered_data = cipher.encrypt(pad(data.encode('utf8'), block_size=32))
    return ciphered_data.hex()


def get_trade_info(order_id: Union[str, int], amount: Union[str, int], email: str) -> str:
    data = {
        'MerchantID': os.environ.get('MerchantID'),
        'RespondType': 'JSON',
        'TimeStamp': int(datetime.now().timestamp()),
        'Version': 1.6,
        'MerchantOrderNo': order_id,
        'Amt': amount,
        'ItemDesc': u'商品資訊',
        'ReturnURL': URL + '/orders/newebpay/return',
        'NotifyURL': URL + '/orders/newebpay/notify',
        'ClientBackURL': URL + f'/orders/{order_id}',
        'Email': email,
        'LoginType': 0,
        'CREDIT': 1
    }

    trade_info = query_string_encode(data)
    return aes_encrypt(trade_info)
