'''Decorators to implement authorization.'''

from functools import wraps
from flask import request
from app.models import User


def login_required(func):
    '''Check if user has a valid token.'''
    @wraps(func)
    def decorated(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        roles = User.decode_token(token=access_token)['roles']
        if ('user' in roles):
                return func(*args, **kwargs)
        return {'message': 'Ensure you have an authorization header.'}, 400
    return decorated


def admin_required(func):
    '''Check if user has a valid admin token.'''

    @wraps(func)
    def decorated(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        roles = User.decode_token(token=access_token)['roles']
        if ('admin' in roles):
            return func(*args, **kwargs)
        return {'message': 'This action requires an admin token.'}, 403
    return decorated
