class UserError(Exception):
    def __init__(self, message):
        self.message = message


class EmailAlreadyUsedError(UserError):
    pass


class DisplayNameAlreadyUsedError(UserError):
    pass
