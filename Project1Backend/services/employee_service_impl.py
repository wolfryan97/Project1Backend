from typing import List

from daos.employee_dao import EmployeeDao
from entities.employee import Employee
from exceptions.employee_not_found import EmployeeNotFoundError
from exceptions.user_pass_incorrect import UsernamePasswordIncorrectError
from services.employee_service import EmployeeService


class EmployeeServiceImpl(EmployeeService):
    def __init__(self, emp_dao: EmployeeDao):
        self.emp_dao = emp_dao

    def create_employee(self, emp: Employee) -> Employee:
        return self.emp_dao.create_employee(emp)

    def get_all_employees(self) -> List[Employee]:
        li: List[Employee] = self.emp_dao.get_all_employees()
        if len(li) == 0:
            raise EmployeeNotFoundError("Error...\nEmployee does not exist.")
        return self.emp_dao.get_all_employees()

    def get_employee(self, emp_id: int) -> Employee:
        try:
            emp = self.emp_dao.get_employee(emp_id)
            if emp is None:
                raise EmployeeNotFoundError("Error...\nEmployee does not exist.")
            return emp
        except IndexError:
            raise EmployeeNotFoundError("Error...\nEmployee does not exist.")

    def remove_employee(self, emp_id: int) -> bool:
        try:
            return self.emp_dao.remove_employee(emp_id)
        except IndexError:
            raise EmployeeNotFoundError("Error...\nEmployee does not exist.")

    def update_employee(self, emp: Employee) -> Employee:
        try:
            return self.emp_dao.update_employee(emp)
        except IndexError:
            raise EmployeeNotFoundError("Error...\nEmployee does not exist.")

    def drop(self):
        return self.emp_dao.drop()

    def recreate(self):
        return self.emp_dao.recreate()

    #  checks if the login credentials belong to a manager
    def login_is_manager(self, username: str, password: str) -> bool:
        try:
            li = self.get_all_employees()
            if len(li) == 0:
                raise UsernamePasswordIncorrectError(
                    "Username or Password is incorrect.\nPlease Enter the correct Username or Password")
            # looks for credentials
            for emp in li:
                if emp.username == username and emp.password == password:
                    return emp.is_manager

            # if reaches here, doesnt exist in system
            raise UsernamePasswordIncorrectError(
                "Username or Password is incorrect.\nPlease Enter the correct Username or Password")

        except IndexError:
            raise UsernamePasswordIncorrectError(
                "Username or Password is incorrect.\nPlease Enter the correct Username or Password")
