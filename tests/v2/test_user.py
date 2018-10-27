"""Test the user view funciton."""
from json import loads, dumps

from .base import BaseCase


class TestUser(BaseCase):
    """User resource tests."""

    def test_create_user(self):
        """Test create  user endpoint."""

        token = self.get_super_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            '/api/v2/users/signup', data=self.user_data_1, headers=headers)
        # self.assertEqual(201, response.status_code)
        expected = {'message': 'User registration successful'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
        self.assertTrue(loads(response.data.decode('utf-8'))['user'])

    def test_duplicate_signup(self):
        token = self.get_super_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            '/api/v2/users/signup', data=self.user_data_1, headers=headers)
        response = self.client.post(
            '/api/v2/users/signup', data=self.user_data_1, headers=headers)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Username already taken, if you are registered,please login to continue.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

    def test_invalid_username(self):
        token = self.get_super_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            '/api/v2/users/signup', data=self.user_data_2, headers=headers)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Invalid username.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

    def test_invalid_email(self):
        # test signup using inavalid email
        token = self.get_super_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            '/api/v2/users/signup', data=self.user_data_3, headers=headers)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Invalid email.Example of a valid one:hero@gmail.com'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

    def test_invalid_password(self):
        # test signup using inavalid password
        
        token = self.get_super_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            '/api/v2/users/signup', data=self.user_data_3, headers=headers)
        self.assertEqual(400, response.status_code)
        expected = {
            'message': 'Invalid password. Password should be 8 or more characters long.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
