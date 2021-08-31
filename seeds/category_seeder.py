from flask_seeder import Seeder, Faker, generator
from models import Category
from seeds.custom_generator import NameSequence


class CategorySeeder(Seeder):
    priority = 5

    def run(self):
        number_of_category_seeds = 5

        faker = Faker(
            cls=Category,
            init={
              'id': generator.Sequence(start=1, end=number_of_category_seeds),
              'name': NameSequence('分類')
            }
        )

        for category in faker.create(number_of_category_seeds):
            print('Adding category: %s' % category)
            self.db.session.add(category)
