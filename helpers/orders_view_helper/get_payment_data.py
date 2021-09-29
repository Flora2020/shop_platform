import os
from datetime import datetime
from typing import Dict, Union


def query_string_encode(data: Dict) -> str:
    key_value_pairs = []
    for key, value in data.items():
        key_value_pairs.append(f'{key}={value}')

    return '&'.join(key_value_pairs)


def get_trade_info(order_id: Union[str, int], amount: Union[str, int], email: str) -> str:
    URL = os.environ.get('URL')
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
    return trade_info
