class EmployeeNotFoundError(Exception):

    description: str = 'Occurs when an employee is not found'

    def __init__(self, message: str):
        self.message = message
