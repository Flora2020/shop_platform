from flask_seeder import Seeder, Faker, generator
from models.user import User
from passlib.hash import pbkdf2_sha256


class Hash(generator.Generator):
    def __init__(self, string, **kwargs):
        super().__init__(**kwargs)
        self.string = string

    def generate(self):
        return pbkdf2_sha256.hash(self.string)


class UserSeeder(Seeder):
    priority = 0

    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=User,
            init={
              'id': generator.Sequence(),
              'display_name': generator.Name(),
              'email': generator.Email(),
              'password': Hash('12345678'),
              'cell_phone': generator.String(pattern='(09)\d{8}'),
              'address': generator.String(pattern='[a-z]{10,50}'),
              'store_introduction': generator.String(pattern='[a-z]{50,1000}'),
              'role': generator.String(pattern='(user|admin)')
            }
        )

        # Create 5 users
        for user in faker.create(5):
            print('Adding user: %s' % user)
            self.db.session.add(user)
