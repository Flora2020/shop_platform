from flask_seeder import generator


class ShippingStatusGenerator(generator.Generator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = -1
        self.shipping_status = ['未出貨', '已出貨', '已到貨', '已取貨']

    def generate(self) -> str:
        self.count += 1
        return self.shipping_status[self.count]
