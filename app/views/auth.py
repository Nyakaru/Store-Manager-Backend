"""User resource."""
import re
from hashlib import sha256

from flask_restful import Resource, reqparse
from app.models import User, db


class AuthResource(Resource):
    """Login user."""

    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, type=str, help='Email (str) is required.')
    parser.add_argument('password', required=True, type=str, help='Password (str) is required.')

    def post(self):
        """Resource for managing user authentication."""

        arguments = AuthResource.parser.parse_args()
        password = arguments.get('password')
        password = sha256(password.encode('utf-8')).hexdigest()
        email = arguments.get('email')
        for user in getattr(db, 'users'):
            if email == user['email'] and password == user['password']:
                new_user = User(**user)
                token = new_user.generate_token()
                return {'message': 'User login successful.', 'token': token }, 200
        return {'message': 'Email/Password Invalid.'}, 400