class RequestNotFoundError(Exception):

    description: str = 'Occurs when a request is not found'

    def __init__(self, message: str):
        self.message = message
