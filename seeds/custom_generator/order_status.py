from flask_seeder import generator


class OrderStatusGenerator(generator.Generator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = -1
        self.order_status = ['未結帳', '已結帳', '申請修改', '已取消']

    def generate(self) -> str:
        self.count += 1
        return self.order_status[self.count]
