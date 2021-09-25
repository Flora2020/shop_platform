from flask_seeder import generator


class PaymentStatusGenerator(generator.Generator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = -1
        self.payment_status = ['未付款', '付款成功', '付款失敗']

    def generate(self) -> str:
        self.count += 1
        return self.payment_status[self.count]
