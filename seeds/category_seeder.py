from flask_seeder import Seeder, Faker, generator
from models import Category
from seeds.custom_generator import NameSequence


class CategorySeeder(Seeder):
    priority = 5

    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=Category,
            init={
              'id': generator.Sequence(),
              'name': NameSequence('分類')
            }
        )

        # Create 5 categories
        for category in faker.create(5):
            print('Adding category: %s' % category)
            self.db.session.add(category)
