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
