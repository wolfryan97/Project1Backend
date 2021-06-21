from typing import List
from daos.employee_dao import EmployeeDao
from entities.employee import Employee
from utils.connection_util import connection


class EmployeeDaoPostgres(EmployeeDao):
    def create_employee(self, emp: Employee) -> Employee:
        sql = """insert into employee (emp_firstname, emp_lastname, is_manager, emp_username, emp_password) values (%s,%s,%s,%s,%s) returning emp_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (
            emp.emp_firstname, emp.emp_lastname, emp.is_manager, emp.username, emp.password
        ))
        connection.commit()
        e_id = cursor.fetchone()[0]
        emp.emp_id = e_id
        return emp

    def get_all_employees(self) -> List[Employee]:
        sql = """select * from employee"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        emp_list = []
        for emp in records:
            emp = Employee(emp[0], emp[1], emp[2], emp[3], emp[4], emp[5])
            emp_list.append(emp)
        return emp_list

    def get_employee(self, emp_id: int) -> Employee:
        sql = """select * from employee where emp_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [emp_id])
        records = cursor.fetchall()
        emp_list = []
        for emp in records:
            emp = Employee(emp[0], emp[1], emp[2], emp[3], emp[4], emp[5])
            emp_list.append(emp)
        return emp_list[0]

    def remove_employee(self, emp_id: int) -> bool:
        self.get_employee(emp_id)  # checks if exists
        sql = """delete from employee where emp_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [emp_id])
        connection.commit()
        return True

    def update_employee(self, emp: Employee) -> Employee:
        self.get_employee(emp.emp_id)  # checks if exists
        sql = """update employee set emp_firstname=%s, emp_lastname=%s, is_manager=%s, emp_username=%s, emp_password=%s where emp_id=%s"""
        cursor = connection.cursor()
        cursor.execute(sql,
                       [emp.emp_firstname, emp.emp_lastname, emp.is_manager,
                        emp.username, emp.password, emp.emp_id])
        connection.commit()
        return emp

    def drop(self):
        sql = """drop table employee"""
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

    def recreate(self):
        sql = """create table employee(emp_id int primary key generated always as identity,emp_firstname varchar(50),emp_lastname varchar(50),is_manager bool,emp_username varchar(50),emp_password varchar(50))"""
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
