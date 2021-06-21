from abc import ABC, abstractmethod
from typing import List

from entities.request import Request


class RequestDao(ABC):
    @abstractmethod
    def create_request(self, req: Request, emp_id: int) -> Request:
        pass

    @abstractmethod
    def get_all_requests(self) -> List[Request]:
        pass

    @abstractmethod
    def get_request(self, req_id: int) -> Request:
        pass

    @abstractmethod
    def get_requests_by_emp_id(self, emp_id: int) -> List[Request]:
        pass

    @abstractmethod
    def remove_request(self, req_id: int) -> bool:
        pass

    @abstractmethod
    def update_request(self, req: Request) -> Request:
        pass

    @abstractmethod
    def drop(self):
        pass

    @abstractmethod
    def recreate(self):
        pass

    @abstractmethod
    def approve(self, req_id: int, msg: str) -> bool:
        pass

    @abstractmethod
    def deny(self, req_id: int, msg: str) -> bool:
        pass
