class Request:
    def __init__(self, req_id: int, emp_id: int, req_amount: float, req_desc: str,
                 req_date: str, approved: bool, mgr_message: str, reviewed: bool):
        self.req_id = req_id
        self.emp_id = emp_id
        self.req_amount = req_amount
        self.req_desc = req_desc
        self.req_date = req_date
        self.approved = approved
        self.mgr_message = mgr_message
        self.reviewed = reviewed

    def json(self):
        return {'reqID': self.req_id,
                'empID': self.emp_id,
                'reqAmount': self.req_amount,
                'reqDesc': self.req_desc,
                'reqDate': self.req_date,
                'approved': self.approved,
                'mgrMessage': self.mgr_message,
                'reviewed': self.reviewed
                }

    @staticmethod
    def json_deserialize(json):
        request = Request(0, 0, 0, '', '', False, '', False)
        request.req_id = json['reqID']
        request.emp_id = json['empID']
        request.req_amount = json['reqAmount']
        request.req_desc = json['reqDesc']
        request.req_date = json['reqDate']
        request.approved = json['approved']
        request.mgr_message = json['mgrMessage']
        request.reviewed = json['reviewed']
        return request
