import time

import pytest

from daos.employee_dao_postgres import EmployeeDaoPostgres
from daos.request_dao_postgres import RequestDaoPostgres
from entities.employee import Employee
from entities.request import Request
from exceptions.employee_not_found import EmployeeNotFoundError
from exceptions.request_not_found import RequestNotFoundError
from exceptions.user_pass_incorrect import UsernamePasswordIncorrectError
from exceptions.wrong_data_type import WrongDataTypeError
from services.employee_service_impl import EmployeeServiceImpl
from services.request_service_impl import RequestServiceImpl

test_emp = Employee(0, "Mister", "Manager", True, "user6", "pass12")
test_emp2 = Employee(0, "Timmy", "Tickles", False, "user77", "pass003")
test_emp3 = Employee(0, "Peter", "Pickles", False, "user101", "pass404")

test_emp_upd = Employee(4, "Senior", "Manager", True, "user88", "pass88")
test_emp_upd2 = Employee(99, "Wolf", "Ryan", True, "user99", "pass99")

employees = [test_emp, test_emp2, test_emp3]

test_req = Request(0, 0, 280, "Hotel expenses for the week of 6/6/21", time.ctime(), False, "", False)
test_req2 = Request(0, 0, 330, "Hotel expenses for the week of 6/13/21", time.ctime(), False, "", False)
test_req3 = Request(0, 0, 195.33, "Food expenses for the week of 6/6/21", time.ctime(), False, "", False)

test_req_upd = Request(5, 0, 330, "Hotel expenses for the week of 6/20/21", time.ctime(), False, "", False)
test_req_upd2 = Request(99, 0, 330, "Hotel expenses for the week of 6/20/21", time.ctime(), False, "", False)
test_req_upd3 = Request(5, 0, "a330", "Hotel expenses for the week of 6/20/21", time.ctime(), False, "",
                        False)  # should fail

requests = [test_req, test_req2, test_req3]

emp_dao = EmployeeDaoPostgres()
req_dao = RequestDaoPostgres()
emp_service = EmployeeServiceImpl(emp_dao)
req_service = RequestServiceImpl(req_dao)


class TestEmployeeService:
    def test_create_employee(self):
        emp_service.create_employee(employees[0])
        emp_service.create_employee(employees[1])
        emp_service.create_employee(employees[2])
        assert emp_service.get_employee(test_emp.emp_id).emp_id == 4

    def test_get_all_employees(self):
        assert len(emp_service.get_all_employees()) == 5

    def test_get_employee(self):
        assert emp_service.get_employee(test_emp3.emp_id).emp_id == test_emp3.emp_id

    def test_get_employee_fail(self):
        with pytest.raises(EmployeeNotFoundError):
            assert emp_service.get_employee(99) == "Error...\nEmployee does not exist."

    def test_remove_emp(self):
        assert emp_service.remove_employee(test_emp3.emp_id) is True

    def test_remove_emp_fail(self):
        with pytest.raises(EmployeeNotFoundError):
            assert emp_service.remove_employee(99) == "Error...\nEmployee does not exist."

    def test_update_client(self):
        assert emp_service.update_employee(test_emp_upd) == test_emp_upd

    def test_update_client_fail(self):
        with pytest.raises(EmployeeNotFoundError):
            assert emp_service.update_employee(test_emp_upd2) == "Error...\nEmployee does not exist."

    def test_login_is_manager(self):
        assert emp_service.login_is_manager(test_emp_upd.username, test_emp_upd.password) is True

    def test_login_is_manager2(self):
        assert emp_service.login_is_manager(test_emp2.username, test_emp2.password) is False

    def test_login_is_manager3(self):
        with pytest.raises(UsernamePasswordIncorrectError):
            assert emp_service.login_is_manager("Not A Valid User", "Not A Valid Pass") == \
                   "Username or Password is incorrect.\nPlease Enter the correct Username or Password"


class TestRequestService:
    def test_create_employee(self):
        req_service.create_request(requests[0], 4)
        req_service.create_request(requests[1], 5)
        req_service.create_request(requests[2], 5)
        assert req_service.get_request(test_req.req_id).req_id == 4

    def test_create_employee2(self):
        with pytest.raises(EmployeeNotFoundError):
            assert req_service.create_request(requests[0], 99) == "Error...\nEmployee does not exist."

    def test_get_all_requests(self):
        assert len(req_service.get_all_requests()) == 5

    def test_get_request(self):
        assert req_service.get_request(test_req3.req_id).req_id == test_req3.req_id

    def test_get_request_fail(self):
        with pytest.raises(RequestNotFoundError):
            assert req_service.get_request(99) == "Error...\nRequest does not exist."

    def test_get_requests_by_emp(self):
        assert req_service.get_requests_by_emp_id(test_emp.emp_id)[0].req_id == test_req.req_id

    def test_get_requests_by_emp_fail(self):
        with pytest.raises(EmployeeNotFoundError):
            assert req_service.get_requests_by_emp_id(99) == "Error...\nEmployee and/or Request does not exist."

    def test_remove_req(self):
        assert req_service.remove_request(test_req3.req_id) is True

    def test_remove_req_fail(self):
        with pytest.raises(RequestNotFoundError):
            assert req_service.remove_request(99) == "Error...\nRequest does not exist."

    def test_update_req(self):
        assert req_service.update_request(test_req_upd).req_id == test_req2.req_id

    def test_update_req_fail(self):
        with pytest.raises(RequestNotFoundError):
            assert req_service.update_request(test_req_upd2) == "Error...\nRequest does not exist."

    def test_update_req_fail2(self):
        with pytest.raises(WrongDataTypeError):
            assert req_service.update_request(test_req_upd3) == "Error...\nPlease use a Float for Amount."
