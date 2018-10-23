'''User resource.'''

import re
from flask_restful import Resource, reqparse
from app.v1.models import User, db


class UserResource(Resource):
    '''Class for handling user registration.'''

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='Username (str) is required.')
    parser.add_argument('email', required=True, type=str, help='Email (str) is required.')
    parser.add_argument('password', required=True, type=str, help='Password (str) is required.')
    parser.add_argument('is_admin', required=False)
    parser.add_argument('is_attendant', required=False)

    def post(self):
        '''Create new user.'''
        arguments = UserResource.parser.parse_args()
        password = arguments.get('password')
        email = arguments.get('email')
        username = arguments.get('username')
        is_admin = arguments.get('is_admin')
        is_attendant = arguments.get('is_attendant')
        email_format = re.compile(r"([a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")
        username_format = re.compile(r"([a-zA-Z0-9]+$)")
        if is_admin or is_attendant:
            if str(is_admin) == 'True' and str(is_attendant) == 'True':
                return {"message": "You are either an admin or an attendant"}, 400
            if str(is_admin) == 'False' and str(is_attendant) == 'False':
                return {"message": "Please pick a role of either admin or attendant"}, 400
            if str(is_admin) == 'True':
                is_attendant = False
            if str(is_attendant) == 'True':
                is_admin = False
            if re.match(username_format, username):
                if re.match(email_format, email):
                    for user in getattr(db, 'users'):
                        if user['email'] == email:
                            return {"message": "username or email already in use"}, 409
                    new_user = User(username=username, password=password, email=email, is_admin=is_admin, is_attendant=is_attendant)
                    new_user.save()
                    return {
                        'message': 'User registration successful',
                        'user': new_user.view()
                        }, 201
                return {"message": "Use a valid email format"}, 400
            return {"message": "Use a username format of alphanumeric"}, 400
        return {"message": "Please pick a role of either admin or attendant"}, 400
