# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from base64 import b64decode
from .errors import token_error


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
                    token_error('Incorrectly formatted token.')
                else:
                    # TODO: Get example token
                    if token == 'token':
                        kwargs['bearer_token'] = token
                        return f(*args, **kwargs)
        return token_error()
    return decorated_function