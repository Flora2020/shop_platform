from wtforms.validators import ValidationError


class ByteLength(object):
    def __init__(self, min: int = -1, max: int = -1, encode: str = 'utf-8', message=None):
        self.min = min
        self.max = max
        self.encode = encode
        if not message:
            message = u'Field must be between %i and %i bytes long.' % (min, max)
        self.message = message

    def __call__(self, form, field):
        length = (field.data and len(field.data.encode(self.encode))) or 0
        if length < self.min or self.max != -1 and length > self.max:
            raise ValidationError(self.message)


byte_length = ByteLength
