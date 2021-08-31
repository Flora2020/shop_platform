from flask_seeder import Seeder, Faker, generator
from models.user import User
from seeds.custom_generator import Hash


class UserSeeder(Seeder):
    priority = 0

    def run(self):
        number_of_user_seeds = 5

        faker = Faker(
            cls=User,
            init={
              'id': generator.Sequence(start=1, end=number_of_user_seeds),
              'display_name': generator.Name(),
              'email': generator.Email(),
              'password': Hash('12345678'),
              'cell_phone': generator.String(pattern='(09)\d{8}'),
              'address': generator.String(pattern='[a-z]{10,50}'),
              'store_introduction': generator.String(pattern='[a-z]{50,1000}'),
              'role': generator.String(pattern='(user|admin)')
            }
        )

        for user in faker.create(number_of_user_seeds):
            print('Adding user: %s' % user)
            self.db.session.add(user)
