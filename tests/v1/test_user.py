"""Test the user view funciton."""
from json import loads, dumps

from .base import BaseCase


class TestUser(BaseCase):
    """User resource tests."""

    def test_create_attendant(self):
        """Test create  user """
        response = self.client.post('/api/v1/users/signup', data=self.store_attendant_user)
        self.assertEqual(201, response.status_code)
        expected = {'message': 'User registration successful'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
    
    def test_create_admin(self):
        """Test create  admin """
        response = self.client.post('/api/v1/users/signup', data=self.admin_user)
        self.assertEqual(201, response.status_code)
        expected = {'message': 'User registration successful'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
    
    def test_duplicate_signup(self):
        # test duplicate signup
        response = self.client.post('/api/v1/users/signup', data=self.store_attendant_user)
        response = self.client.post('/api/v1/users/signup', data=self.store_attendant_user)
        self.assertEqual(409, response.status_code)
        expected = {'message': "username or email already in use"}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])

    def test_user_invalid_email(self):
        """Test invalid email """
        response = self.client.post('/api/v1/users/signup', data=self.user_data_3)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'Invalid email format'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
    
    def test_user_invalid_username(self):
        """Test invalid username """
        response = self.client.post('/api/v1/users/signup', data=self.user_data_2)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'bad username format'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
    
    def test_missing_roles(self):
        """Test missing roles """
        response = self.client.post('/api/v1/users/signup', data=self.user_data_4)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'pick a role'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
    
    def test_roles(self):
        """Test roles """
        response = self.client.post('/api/v1/users/signup', data=self.user_data_5)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'pick a role'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
    
    def test_duplicate_roles(self):
        """Test duplicate roles """
        response = self.client.post('/api/v1/users/signup', data=self.user_data_6)
        self.assertEqual(400, response.status_code)
        expected = {'message': 'one at a time'}
        self.assertEqual(expected['message'], loads(
            response.data.decode('utf-8'))['message'])
