from flask_seeder import Seeder, Faker, generator
from models import PaymentStatus
from seeds.custom_generator import PaymentStatusGenerator


class ShippingStatusSeeder(Seeder):
    priority = 20

    def run(self):
        number_of_payment_status_seeds = 3

        faker = Faker(
            cls=PaymentStatus,
            init={
                'id': generator.Sequence(start=1, end=number_of_payment_status_seeds),
                'status': PaymentStatusGenerator()
            }
        )

        for status in faker.create(number_of_payment_status_seeds):
            print('Adding payment status: %s' % status)
            self.db.session.add(status)
