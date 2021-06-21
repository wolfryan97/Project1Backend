import time

from daos.employee_dao import EmployeeDao
from daos.employee_dao_postgres import EmployeeDaoPostgres
from daos.request_dao import RequestDao
from daos.request_dao_postgres import RequestDaoPostgres
from entities.employee import Employee
from entities.request import Request

emp_dao: EmployeeDao = EmployeeDaoPostgres()
req_dao: RequestDao = RequestDaoPostgres()

# recreate databases before testing
req_dao.drop()
emp_dao.drop()
emp_dao.recreate()
req_dao.recreate()

test_emp = Employee(0, "Wolf", "Ryan", True, "user", "pass")
test_emp2 = Employee(0, "Ed", "McEmployee", False, "user1", "pass2")
test_emp3 = Employee(0, "JJ", "Louis", False, "user2", "pass2")

test_emp_upd = Employee(1, "Wolf", "Ryan", True, "user", "pass")

test_req = Request(0, 0, 280, "Hotel expenses for the week of 6/6/21", time.ctime(), False, "", False)
test_req2 = Request(0, 0, 330, "Hotel expenses for the week of 6/13/21", time.ctime(), False, "", False)
test_req3 = Request(0, 0, 195.33, "Food expenses for the week of 6/6/21", time.ctime(), False, "", False)

test_req_upd = Request(2, 0, 330, "Hotel expenses for the week of 6/20/21", time.ctime(), False, "", False)


class TestEmployeeDao:
    # successful creation
    def test_create_emp(self):
        assert emp_dao.create_employee(test_emp).emp_id == test_emp.emp_id

    def test_create_emp2(self):
        assert emp_dao.create_employee(test_emp2).emp_id == test_emp2.emp_id

    def test_get_all_employees(self):
        assert len(emp_dao.get_all_employees()) == 2

    # get emp by id
    def test_get_employee(self):
        assert emp_dao.get_employee(2).emp_id == test_emp2.emp_id

    def test_remove_emp(self):
        emp_dao.create_employee(test_emp3)
        assert emp_dao.remove_employee(3) is True

    def test_update_client(self):
        assert emp_dao.update_employee(test_emp_upd) == test_emp_upd


class TestRequestDao:
    # successful creation
    def test_create_req(self):
        assert req_dao.create_request(test_req, test_emp.emp_id).emp_id == test_req.req_id

    def test_create_req2(self):
        assert req_dao.create_request(test_req2, test_emp2.emp_id).emp_id == test_req2.req_id

    def test_get_all_requests(self):
        assert len(req_dao.get_all_requests()) == 2

    def test_get_request(self):
        assert req_dao.get_request(test_req.req_id).req_id == test_req.req_id

    def test_get_requests_by_emp(self):
        assert req_dao.get_requests_by_emp_id(test_emp.emp_id)[0].req_id == test_req.emp_id

    def test_remove_req(self):
        req_dao.create_request(test_req3, test_emp2.emp_id)
        assert req_dao.remove_request(test_req3.req_id) is True

    def test_update_req(self):
        assert req_dao.update_request(test_req_upd).req_id == req_dao.get_request(test_req2.req_id).req_id

    def test_approve(self):
        assert req_dao.approve(test_req2.req_id, "") == (req_dao.get_request(test_req2.req_id).approved is True)

    def test_deny(self):
        assert req_dao.deny(test_req2.req_id, "pytest") == (req_dao.get_request(test_req2.req_id).approved is False)
