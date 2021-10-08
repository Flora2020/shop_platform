from dataclasses import dataclass, field
from typing import Tuple


@dataclass(eq=False)
class FlashMessage:
    message: str = field(default='')
    category: str = field(default='')

    def __repr__(self):
        return f'<FlashMessage message: {self.message}, category: {self.category}>'

    def to_tuple(self) -> Tuple[str, str]:
        return self.message, self.category


product_not_found = FlashMessage('查無此商品', 'warning').to_tuple()
seller_products_not_found = FlashMessage('查無此賣家商品，返回商城首頁', 'warning').to_tuple()
register_success = FlashMessage('註冊成功', 'success').to_tuple()
login_success = FlashMessage('登入成功', 'success').to_tuple()
login_required_msg = FlashMessage('需要先登入才能使用此功能', 'warning').to_tuple()
logout_success = FlashMessage('登出成功', 'success').to_tuple()
product_update_success = FlashMessage('商品更新成功', 'success').to_tuple()
cart_is_empty = FlashMessage('購物車中沒有商品', 'success').to_tuple()
order_not_found = FlashMessage('查無此訂單', 'warning').to_tuple()
order_complete = FlashMessage('訂單成立', 'success').to_tuple()
order_cannot_modify = FlashMessage('訂單已結帳或已取消，無法修改', 'warning').to_tuple()
trade_info_invalid = FlashMessage('交易資訊異常，請等候信件通知', 'warning').to_tuple()
paid_order_not_found = FlashMessage('查無此訂單，請等候信件通知', 'warning').to_tuple()
payment_fail = FlashMessage('付款失敗，請稍後再試', 'warning').to_tuple()
wrong_payment_amount = FlashMessage('付款金額與訂單不符，請等候信件通知', 'warning').to_tuple()
payment_success = FlashMessage('付款成功！', 'success').to_tuple()
cannot_cancel_canceled_order = FlashMessage('無法取消「已取消」之訂單', 'warning').to_tuple()
cannot_cancel_paid_order = FlashMessage('無法取消「已付款」之訂單', 'warning').to_tuple()
only_backlog_order_is_cancelable = FlashMessage('只能取消「未出貨」之訂單', 'warning').to_tuple()
order_canceled = FlashMessage('訂單已取消', 'success').to_tuple()
