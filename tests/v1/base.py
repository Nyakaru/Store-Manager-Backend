'''Base test class.'''
from unittest import TestCase
from json import dumps

from app.v1.models import db, Product, Sale, User
from app import create_app

class BaseCase(TestCase):
    '''Base class to be inherited by all other testcases.'''

    def setUp(self):
        '''Set up test application.'''
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.admin_user = {
            'username': 'Nyakaru',
            'email': 'nyakaru@gmail.com',
            'password': 'password',
            'is_admin': True,
            'is_attendant': False
        }
        self.store_attendant_user = {
            'username': 'Nyakaru',
            'email': 'nyakaru@gmail.com',
            'password': 'password',
            'is_admin': False,
            'is_attendant': True
        }
        self.user_data_2 = {
            'username': '',
            'email': 'user2@mail.com',
            'password': 'password',
            'is_admin': False,
            'is_attendant': True
        }
        self.user_data_3 = {
            'username': 'user3',
            'email': 'user2mail.com',
            'password': 'password',
            'is_admin': False,
            'is_attendant': True
        }
        self.user_data_4 = {
            'username': 'user4',
            'email': 'user2@mail.com',
            'password' :'password'
        }
        self.user_data_5 = {
            'username': 'user5',
            'email': 'user2@mail.com',
            'password': 'password',
            'is_admin': False,
            'is_attendant': False
        }
        self.user_data_6 = {
            'username': 'user5',
            'email': 'user2@mail.com',
            'password': 'password',
            'is_admin': True,
            'is_attendant': True
        }
        self.valid_product_data = {
            'name': 'tea',
            'price': 45
        }
        self.invalid_product_name = {
            'name': '**',
            'price': 40
        }
        self.invalid_product_price_data = {
            'name': 'bread',
            'price': 'vhjk'
        }
        self.headers = {'Content-Type': 'application/json'}


    def get_admin_token(self):
        '''Create an admin token for testing.'''
        self.client.post('api/v1/users/signup', data=dumps(self.admin_user), headers=self.headers)
        res = self.client.post('api/v1/users/signin', data=dumps(self.admin_user), headers=self.headers)
        return res.json['token']


    def get_attendant_token(self):
        '''Create an attendant token for testing.'''
        self.client.post('api/v1/users/signup', data=dumps(self.store_attendant_user), headers=self.headers)
        res = self.client.post('api/v1/users/signin', data=dumps(self.store_attendant_user), headers=self.headers)
        return res.json['token']

    def tearDown(self):
        '''Delete database and recreate it with no data.'''
        db.drop()
        self.app_context.pop()
