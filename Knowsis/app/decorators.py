# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from base64 import b64decode
from .exceptions import Unauthorized


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization', None)
        if authorization_header is not None:
            split_header = authorization_header.split(' ')
            if len(split_header) == 2 and split_header[0] == 'Bearer':
                encoded_token = split_header[1]
                try:
                    token = unicode(b64decode(encoded_token))
                except (TypeError, UnicodeDecodeError):
                    raise Unauthorized('Incorrectly formatted token', status_code=401)
                else:
                    # Coded token = 'YjdiZWU4MzNmNGU5MGJiYzNmYTk3MmIwYzkwMWEwZGM='
                    # TODO: Get example token
                    if token == 'b7bee833f4e90bbc3fa972b0c901a0dc':
                        kwargs['bearer_token'] = token
                        return f(*args, **kwargs)
        raise Unauthorized('Invalid token', status_code=401)
    return decorated_function
