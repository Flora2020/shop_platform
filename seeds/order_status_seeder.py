from flask_seeder import Seeder, Faker, generator
from models import OrderStatus
from seeds.custom_generator import OrderStatusGenerator


class ShippingStatusSeeder(Seeder):
    priority = 25

    def run(self):
        number_of_order_status_seeds = 4

        faker = Faker(
            cls=OrderStatus,
            init={
                'id': generator.Sequence(start=1, end=number_of_order_status_seeds),
                'status': OrderStatusGenerator()
            }
        )

        for status in faker.create(number_of_order_status_seeds):
            print('Adding order status: %s' % status)
            self.db.session.add(status)
