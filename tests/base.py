'''Base test class.'''
from unittest import TestCase

from app.models import db, Product, Sale, User
from app import create_app

class BaseCase(TestCase):
    '''Base class to be inherited by all other testcases.'''

    def setUp(self):
        '''Set up test application.'''
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user1 = User(
            username='user1',
            email='user1@email.com',
            password='pass#123')
        self.user1.save()

        self.user_data_1 = {
            'username': 'user',
            'email': 'user@mail.com',
            'password': 'password'
        }

        self.user_data_2 = {
            'username': '',
            'email': 'user2@mail.com',
            'password': 'password'
        }

        self.user_data_3 = {
            'username': 'user3',
            'email': 'user2mail.com',
            'password': 'password'
        }
        self.product1 = Product(
            name='Product1',
            price=100
        )
        self.product1.save()
        self.valid_product_data = {
            'name': 'Product2',
            'price': 100
        }
        self.invalid_product_data = {
            'name': None,
            'price': None
        }

        self.invalid_product_data_name = {
            'name': "",
            'price': 100
        }
        self.product1.save()
        self.sale1 = Sale({1: 2})
        self.sale1.save()

    def get_user_token(self):
        '''Create a token for testing.'''

        self.user1.roles.append('user')
        self.user1.save()
        return self.user1.generate_token()

    def get_admin_token(self):
        '''Create an admin token for testing.'''

        admin = User(
            username='admin', password='pass1234', email='admin@mail.com')
        admin.roles.extend(['admin', 'user'])
        admin.save()
        return admin.generate_token()

    def tearDown(self):
        '''Delete database and recreate it with no data.'''
        db.drop()
        self.app_context.pop()
