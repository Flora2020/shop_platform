from random import randint
from flask_seeder import generator


class ImageUrl(generator.Generator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate(self) -> str:
        return f'https://loremflickr.com/320/240?lock={randint(1, 10000)}'
