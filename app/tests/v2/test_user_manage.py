"""Test the user management funciton."""
from json import loads, dumps

from .base import BaseCase

MNG_URL = '/api/v2/users/manage/1'


class TestUserManagement(BaseCase):
    '''Test promoting a user.'''

    def test_user_can_be_promoted(self):
        # create user
        self.user1.add_user()
        token = self.get_super_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        # test user promoted
        response = self.client.put(MNG_URL, headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_promoting_non_user(self):
        token = self.get_super_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.put('/api/v2/users/manage/10', headers=headers)
        expected = {'message': "User was not found!"}
        self.assertEqual(expected, loads(response.data.decode()))
        self.assertEqual(response.status_code, 404)
