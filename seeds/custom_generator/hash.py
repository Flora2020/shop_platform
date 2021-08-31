from flask_seeder import generator
from passlib.hash import pbkdf2_sha256


class Hash(generator.Generator):
    def __init__(self, string: str, **kwargs):
        super().__init__(**kwargs)
        self.string = string

    def generate(self) -> str:
        return pbkdf2_sha256.hash(self.string)
