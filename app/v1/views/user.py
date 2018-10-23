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
    parser.add_argument('isAdmin', required=False)
    parser.add_argument('isAttendant', required=False)

    def post(self):
        '''Create new user.'''
        arguments = UserResource.parser.parse_args()
        password = arguments.get('password')
        email = arguments.get('email')
        username = arguments.get('username')
        isAdmin = arguments.get('isAdmin')
        isAttendant = arguments.get('isAttendant')
        email_format = re.compile(r"([a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")
        username_format = re.compile(r"([a-zA-Z0-9]+$)")
        if isAdmin or isAttendant:
            if str(isAdmin) == 'True' and str(isAttendant) == 'True':
                return {"message": "one at a time"}, 400
            if str(isAdmin) == 'False' and str(isAttendant) == 'False':
                return {"message": "pick a role"}, 400
            if str(isAdmin) == 'True':
                isAttendant = False
            if str(isAttendant) == 'True':
                isAdmin = False
            if re.match(username_format, username):
                if re.match(email_format, email):
                    for user in getattr(db, 'users'):
                        if user['email'] == email:
                            return {"message": "username or email already in use"}, 409
                    new_user = User(username=username, password=password, email=email, isAdmin=isAdmin, isAttendant=isAttendant)
                    new_user.save()
                    return {
                        'message': 'User registration successful',
                        'user': new_user.view()
                        }, 201
                return {"message": "Use a valid email format"}, 400
            return {"message": "Use a username format of alphanumeric"}, 400
        return {"message": "pick a role"}, 400
