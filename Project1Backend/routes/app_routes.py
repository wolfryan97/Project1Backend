from flask import Flask, request, jsonify

from daos.employee_dao import EmployeeDao
from daos.employee_dao_postgres import EmployeeDaoPostgres
from daos.request_dao import RequestDao
from daos.request_dao_postgres import RequestDaoPostgres
from entities.employee import Employee
from entities.request import Request
from exceptions.employee_not_found import EmployeeNotFoundError
from exceptions.request_not_found import RequestNotFoundError
from services.employee_service import EmployeeService
from services.employee_service_impl import EmployeeServiceImpl
from services.request_service import RequestService
from services.request_service_impl import RequestServiceImpl

emp_dao: EmployeeDao = EmployeeDaoPostgres()
req_dao: RequestDao = RequestDaoPostgres()
emp_service: EmployeeService = EmployeeServiceImpl(emp_dao)
req_service: RequestService = RequestServiceImpl(req_dao)


def create_routes(app: Flask):
    @app.post('/employees')
    def create_employee():
        emp = Employee.json_deserialize(request.json)
        emp_service.create_employee(emp)
        app.logger.info(f'New employee registered ID: {emp.emp_id}.')
        return jsonify(emp.json()), 201

    @app.get('/employees')
    def get_all_employees():
        try:
            emps = emp_service.get_all_employees()
            dict_list = [emp.json() for emp in emps]
            return jsonify(dict_list), 200
        except EmployeeNotFoundError as e:
            return e.message, 404

    @app.get('/employees/<emp_id>')
    def get_employee_by_id(emp_id: str):
        try:
            e = emp_service.get_employee(int(emp_id))
            return jsonify(e.json()), 200
        except EmployeeNotFoundError as e:
            return e.message, 404

    @app.put('/employees/<emp_id>')
    def update_employee(emp_id: str):
        try:
            emp = Employee.json_deserialize(request.json)
            emp.emp_id = int(emp_id)
            emp_service.update_employee(emp)
            return jsonify(emp.json()), 200
        except EmployeeNotFoundError as e:
            return e.message, 404

    @app.delete('/employees/<emp_id>')
    def remove_employee(emp_id: str):
        try:
            emp_service.remove_employee(int(emp_id))
            app.logger.info(f'Deleted employee ID: {emp_id}')
            return f'Employee ID: {emp_id} deleted.', 205
        except EmployeeNotFoundError as e:
            return e.message, 404

    @app.post('/employees/<emp_id>/requests')
    def create_request(emp_id: str):
        try:
            req = Request.json_deserialize(request.json)
            req_service.create_request(req, int(emp_id))
            app.logger.info(f'New request registered ID: {req.req_id}')
            return jsonify(req.json()), 201
        except EmployeeNotFoundError as e:
            return e.message, 404

    @app.get('/employees/<emp_id>/requests')
    def get_requests_by_emp_id(emp_id: str):
        try:
            requests = req_service.get_requests_by_emp_id(int(emp_id))
            dict_list = [req.json() for req in requests]
            return jsonify(dict_list), 200
        except EmployeeNotFoundError as e:
            return e.message, 404

    @app.get('/employees/<emp_id>/requests/<req_id>')
    def get_request(emp_id: str, req_id: str):
        try:
            req = req_service.get_request(int(req_id))
            if req.emp_id == int(emp_id):
                return jsonify(req.json()), 200
            else:  # request belongs to another client
                return "Request exists for another Employee", 404
        except RequestNotFoundError as e:
            return e.message, 404

    @app.put('/employees/<emp_id>/requests/<req_id>')
    def update_request(emp_id: str, req_id: str):
        try:
            r = req_service.get_request(int(req_id))
            if r.emp_id == int(emp_id):
                req = Request.json_deserialize(request.json)
                req.emp_id = int(emp_id)
                req.req_id = int(req_id)
                req_service.update_request(req)
                return jsonify(req.json()), 200
            else:
                return "Request exists for another Employee", 404
        except RequestNotFoundError as e:
            return e.message, 404

    @app.delete('/employees/<emp_id>/requests/<req_id>')
    def remove_request(emp_id: str, req_id: str):
        try:
            if req_service.get_request(int(req_id)).emp_id == int(emp_id):
                req_service.remove_request(int(req_id))
                app.logger.info(f'Deleted request ID: {req_id}')
                return f'Request ID: {req_id} deleted.', 205
            else:
                return "Request does not exist for that employee.", 404
        except RequestNotFoundError as e:
            return e.message, 404

    @app.patch('/employees/<emp_id>/requests/<req_id>/approve')
    def approve(emp_id: str, req_id: str):
        msg = request.args.get('msg')
        msg_txt = ""
        if msg is not None:
            msg_txt = msg
        try:
            # Will always pass
            req = req_service.get_request(int(req_id))
            if req.emp_id != int(emp_id):
                return "Request does not exist for that employee.", 404
            req.approved = True
            req.reviewed = True
            req_service.approve(int(req_id), msg_txt)
            return jsonify(req.json()), 200
        except RequestNotFoundError as e:
            return e.message, 404

    @app.patch('/employees/<emp_id>/requests/<req_id>/deny')
    def deny(emp_id: str, req_id: str):
        msg = request.args.get('msg')
        msg_txt = ""
        if msg is not None:
            msg_txt = msg
        try:
            # Will always pass
            req = req_service.get_request(int(req_id))
            if req.emp_id != int(emp_id):
                return "Request does not exist for that employee.", 404
            req.approved = False
            req.reviewed = True
            req_service.deny(int(req_id), msg_txt)
            return jsonify(req.json()), 200
        except RequestNotFoundError as e:
            return e.message, 404
