import time
from typing import List

from daos.employee_dao_postgres import EmployeeDaoPostgres
from daos.request_dao import RequestDao
from entities.request import Request
from utils.connection_util import connection


class RequestDaoPostgres(RequestDao):
    def create_request(self, req: Request, emp_id) -> Request:
        emp_dao = EmployeeDaoPostgres()
        emp_dao.get_employee(emp_id)  # checks if emp exists
        sql = """insert into request (emp_id, amount, description, req_date, approved, mgr_message, reviewed) values (%s,%s,%s,%s,%s,%s,%s) returning req_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (emp_id, req.req_amount, req.req_desc,
                             time.ctime(), False, req.mgr_message, False))
        connection.commit()
        r_id = cursor.fetchone()[0]
        req.req_id = r_id
        req.emp_id = emp_id
        return req

    def get_all_requests(self) -> List[Request]:
        sql = """select * from request"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        req_list = []
        for req in records:
            req = Request(req[0], req[1], req[2], req[3], req[4], req[5], req[6], req[7])
            req_list.append(req)
        return req_list

    def get_request(self, req_id: int) -> Request:
        sql = """select * from request where req_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [req_id])
        records = cursor.fetchall()

        for x in records:
            req = Request(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
            if x[0] == req_id:
                return req

    def get_requests_by_emp_id(self, emp_id: int) -> List[Request]:
        sql = """select * from request where emp_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [emp_id])
        records = cursor.fetchall()

        req_list = []
        for req in records:
            req = Request(req[0], req[1], req[2], req[3], req[4], req[5], req[6], req[7])
            req_list.append(req)
        return req_list

    def remove_request(self, req_id: int) -> bool:
        check = self.get_request(req_id)  # checks if exists
        sql = """delete from request where req_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [req_id])
        connection.commit()
        return True if check else False

    def update_request(self, req: Request) -> Request:
        check = self.get_request(req.req_id)  # checks if exists

        sql = """update request set amount=%s, description=%s, req_date=%s, approved=%s, mgr_message=%s, reviewed=%s where req_id=%s"""
        cursor = connection.cursor()
        int(req.req_amount)  # test to see if is int
        cursor.execute(sql, (req.req_amount, req.req_desc, time.ctime(), req.approved, req.mgr_message, req.reviewed, req.req_id))
        connection.commit()
        return req if check else None

    def drop(self):
        sql = """drop table request"""
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

    def recreate(self):
        sql = """create table request(req_id int primary key generated always as identity,emp_id int,amount float,description varchar(150),req_date varchar(50),approved bool,mgr_message varchar(150),reviewed bool,constraint fk_emp_id foreign key (emp_id) references employee(emp_id))"""
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return True

    def approve(self, req_id: int, msg: str) -> bool:
        check = self.get_request(req_id)  # checks if exists
        sql ="""update request set approved = %s, reviewed = %s, mgr_message = %s where req_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (True, True, msg, req_id))
        connection.commit()
        return True if check else False

    def deny(self, req_id: int, msg: str) -> bool:
        check = self.get_request(req_id)  # checks if exists
        sql ="""update request set approved = %s, reviewed = %s, mgr_message = %s where req_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (False, True, msg, req_id))
        connection.commit()
        return True if check else False
