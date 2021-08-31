from flask_seeder import Seeder, Faker, generator
from models import Product
from seeds.custom_generator import ImageUrl, ChineseTextHolder, NameSequence


class ProductSeeder(Seeder):
    priority = 10

    def run(self):
        number_of_user_seeds = 5
        number_of_category_seeds = 5
        number_of_product_seeds = 100

        faker = Faker(
            cls=Product,
            init={
                'id': generator.Sequence(start=1, end=number_of_product_seeds),
                'name': NameSequence('商品'),
                'price': generator.Integer(start=50, end=50000),
                'image_url': ImageUrl(),
                'inventory': generator.Integer(start=10, end=200),
                'description': ChineseTextHolder(100, 500),
                'seller_id': generator.Integer(start=1, end=number_of_user_seeds),
                'category_id': generator.Integer(start=1, end=number_of_category_seeds)
            }
        )

        for product in faker.create(number_of_product_seeds):
            print('Adding product: %s' % product)
            self.db.session.add(product)
