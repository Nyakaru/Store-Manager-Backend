"""Test the user view funciton."""
from json import loads, dumps

from .base import BaseCase


class TestAuth(BaseCase):
    """User resource tests."""

    def test_auth_user(self):
        '''test correct signin'''
        response = self.client.post('/api/v1/users/signup', data=self.store_attendant_user)
        response = self.client.post('/api/v1/users/signin', data={'email': 'nyakaru@gmail.com', 'password': 'password'})
        self.assertEqual(200, response.status_code)
        expected = {'message': 'User login successful.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
        self.assertTrue(loads(response.data.decode('utf-8'))['token'])
    
    def test_wrong_password(self):
        ''' test signin with wrong password'''
        response = self.client.post(
            '/api/v1/users/signin',data={'email': 'nyakaru@gmail.com', 'password': 'pass#1234'})
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Email/Password Invalid.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

    def test_nonexistent_email(self):
        '''test signin with nonexistent email'''
        response = self.client.post(
            '/api/v1/users/signin',
            data={'email': 'user8@gmail.com', 'password': 'pass#1234'})
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Email/Password Invalid.'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
        