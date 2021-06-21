from typing import List

from daos.request_dao import RequestDao
from entities.request import Request
from exceptions.employee_not_found import EmployeeNotFoundError
from exceptions.request_not_found import RequestNotFoundError
from exceptions.wrong_data_type import WrongDataTypeError
from services.request_service import RequestService


class RequestServiceImpl(RequestService):
    def __init__(self, req_dao: RequestDao):
        self.req_dao = req_dao

    def create_request(self, req: Request, emp_id: int) -> Request:
        try:
            return self.req_dao.create_request(req, emp_id)
        except IndexError:
            raise EmployeeNotFoundError("Error...\nEmployee does not exist.")

    def get_all_requests(self) -> List[Request]:
        li: List[Request] = self.req_dao.get_all_requests()
        if len(li) == 0:
            raise RequestNotFoundError("Error...\nRequest does not exist.")
        return li

    def get_request(self, req_id: int) -> Request:
        try:
            req = self.req_dao.get_request(req_id)
            if req is None:
                raise RequestNotFoundError("Error...\nRequest does not exist.")
            return req
        except IndexError:
            raise RequestNotFoundError("Error...\nRequest does not exist.")

    def get_requests_by_emp_id(self, emp_id: int) -> List[Request]:
        try:
            li = self.req_dao.get_requests_by_emp_id(emp_id)
            if len(li) == 0:
                raise EmployeeNotFoundError("Error...\nEmployee does not exist.")
            return li
        except IndexError:
            raise EmployeeNotFoundError("Error...\nEmployee does not exist.")

    def remove_request(self, req_id: int) -> bool:
        try:
            req = self.req_dao.remove_request(req_id)
            if req is False:
                raise RequestNotFoundError("Error...\nRequest does not exist.")
            return req
        except IndexError:
            raise RequestNotFoundError("Error...\nRequest does not exist.")

    def update_request(self, req: Request) -> Request:
        try:
            req = self.req_dao.update_request(req)
            if req is None:
                raise RequestNotFoundError("Error...\nRequest does not exist.")
            return req
        except IndexError:
            raise RequestNotFoundError("Error...\nRequest does not exist.")
        except TypeError:
            raise WrongDataTypeError("Error...\nPlease use a Float for Amount.")
        except ValueError:
            raise WrongDataTypeError("Error...\nPlease use a Float for Amount.")

    def drop(self):
        return self.req_dao.drop()

    def recreate(self):
        return self.req_dao.recreate()

    def approve(self, req_id: int, msg: str) -> bool:
        try:
            return self.req_dao.approve(req_id, msg)
        except Exception:
            raise RequestNotFoundError("Should theoretically never trip. The mgr will already "
                                       "have access to the acct id at this point")

    def deny(self, req_id: int, msg: str) -> bool:
        try:
            return self.req_dao.deny(req_id, msg)
        except Exception:
            raise RequestNotFoundError("Should theoretically never trip. The mgr will already "
                                       "have access to the acct id at this point")
