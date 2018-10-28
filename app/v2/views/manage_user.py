'''User management resource.'''

import re
from flask import request
from flask_restful import Resource, reqparse

from app.v2.models.user_models import User, UserRoles
from app.v2.decorators import super_user_required


class DBManageUsersResource(Resource):
    '''Resource for managing users an admin.'''

    #@super_user_required
    def put(self, user_id):
        '''Method for editing user roles to include admin'''
        user = User.get(id=user_id)
        if user:
            # check if a user i already an admin
            user_roles = UserRoles.get_user_roles(user[0])
            if 'admin' not in user_roles:
                User.make_user_admin(user_id)
                return{'message': "User has been made admin successfully!"}, 200
            return{"message": "User {} is already an admin.".format(user_id)}
        return{'message': "User was not found!"}, 404
