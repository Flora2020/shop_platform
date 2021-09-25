from flask_seeder import Seeder, Faker, generator
from models import ShippingStatus
from seeds.custom_generator import ShippingStatusGenerator


class ShippingStatusSeeder(Seeder):
    priority = 15

    def run(self):
        number_of_shipping_status_seeds = 4

        faker = Faker(
            cls=ShippingStatus,
            init={
                'id': generator.Sequence(start=1, end=number_of_shipping_status_seeds),
                'status': ShippingStatusGenerator()
            }
        )

        for status in faker.create(number_of_shipping_status_seeds):
            print('Adding shipping status: %s' % status)
            self.db.session.add(status)
