class Employee:
    def __init__(self, emp_id: int, emp_firstname: str, emp_lastname: str,
                 is_manager: bool, username: str, password: str):
        self.emp_id = emp_id
        self.emp_firstname = emp_firstname
        self.emp_lastname = emp_lastname
        self.is_manager = is_manager
        self.username = username
        self.password = password

    def __str__(self):
        return f"Employee ID: {self.emp_id}\nName: {self.emp_firstname} {self.emp_lastname}"

    def json(self):
        return {'empID': self.emp_id,
                'firstname': self.emp_firstname,
                'lastname': self.emp_lastname,
                'isManager': self.is_manager,
                'username': self.username,
                'password': self.password
                }

    @staticmethod
    def json_deserialize(json):
        employee = Employee(0, '', '', False, '', '')
        employee.emp_id = json['empID']
        employee.emp_firstname = json['firstname']
        employee.emp_lastname = json['lastname']
        employee.is_manager = json['isManager']
        employee.username = json['username']
        employee.password = json['password']
        return employee
