import os
from flask_seeder import Seeder, Faker, generator
from models import Category


class CategoryName(generator.Generator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    @staticmethod
    def read_resource(path):
        path = os.path.dirname(os.path.abspath(__file__)) + path
        print(path)
        with open(path) as source:
            lines = source.read().splitlines()

        return lines

    def generate(self):
        if self._lines is None:
            self._lines = self.read_resource('/data/categories.txt')
        result = self.rnd.choice(self._lines)

        return result


class CategorySeeder(Seeder):
    priority = 5

    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=Category,
            init={
              'id': generator.Sequence(),
              'name': CategoryName()
            }
        )

        # Create 5 categories
        for category in faker.create(5):
            print('Adding category: %s' % category)
            self.db.session.add(category)
