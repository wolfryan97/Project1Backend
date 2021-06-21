from abc import ABC, abstractmethod
from typing import List
from entities.employee import Employee


class EmployeeService(ABC):
    @abstractmethod
    def create_employee(self, emp: Employee) -> Employee:
        pass

    @abstractmethod
    def get_all_employees(self) -> List[Employee]:
        pass

    @abstractmethod
    def get_employee(self, emp_id: int) -> Employee:
        pass

    @abstractmethod
    def remove_employee(self, emp_id: int) -> bool:
        pass

    @abstractmethod
    def update_employee(self, emp: Employee) -> Employee:
        pass

    @abstractmethod
    def drop(self):
        pass

    @abstractmethod
    def recreate(self):
        pass

    @abstractmethod
    def login_is_manager(self, username: str, password: str):
        pass
