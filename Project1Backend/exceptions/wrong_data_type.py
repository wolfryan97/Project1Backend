class WrongDataTypeError(Exception):

    description: str = 'Occurs when a wrong data type is entered for amount'

    def __init__(self, message: str):
        self.message = message
