class UsernamePasswordIncorrectError(Exception):

    description: str = 'Occurs when login credentials are incorrect'

    def __init__(self, message: str):
        self.message = message
