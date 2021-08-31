from flask_seeder import generator


class NameSequence(generator.Generator):
    def __init__(self, name: str = 'name', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.count = 0

    def generate(self) -> str:
        self.count += 1
        return f'{self.name} {self.count}'
