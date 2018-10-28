'''Decorators to implement authorization.'''
from functools import wraps
import jwt

from flask import request
from app.v1.models import User


def login_required(func):
    '''Check if user has a valid token.'''
    @wraps(func)
    def decorated(*args, **kwargs):
        '''Decorator for store attendant'''
        try:
            access_token = request.headers.get('Authorization')
            is_attendant = User.decode_token(token=access_token)['is_attendant']
            if is_attendant:
                return func(*args, **kwargs)
            return {'message': 'You have insufficient permissions.'}, 403
        except jwt.exceptions.DecodeError:
            return {"message": "please provide a token"}, 401
    return decorated


def admin_required(func):
    '''Check if user has a valid admin token.'''

    @wraps(func)
    def decorated(*args, **kwargs):
        '''Decorator for store admin'''
        try:
            access_token = request.headers.get('Authorization')
            is_admin = User.decode_token(token=access_token)['is_admin']
            if is_admin:
                return func(*args, **kwargs)
            return {'message': 'You have insufficient permissions.'}, 403
        except jwt.exceptions.DecodeError:
            return {"message": "please provide a token"}, 401
    return decorated
