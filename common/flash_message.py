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
