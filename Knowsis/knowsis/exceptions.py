# -*- coding: utf-8 -*-

class BadRequest(Exception):

    status_code = 400

    def __init__(self, message='Bad request', status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        data = dict(self.payload or ())
        data['error_message'] = self.message
        return data


class Unauthorized(Exception):

    status_code = 401

    def __init__(self, message='Unauthorized', status_code=401, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        data = dict(self.payload or ())
        data['error_message'] = self.message
        return data
