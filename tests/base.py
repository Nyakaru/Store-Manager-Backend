'''Base test class.'''
from unittest import TestCase


from app.models import db, Product, Sale
from app import create_app


class BaseCase(TestCase):
    '''Base class to be inherited by all other testcases.'''

    def setUp(self):
        '''Set up test application.'''
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
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
    def tearDown(self):
        '''Delete database and recreate it with no data.'''
        db.drop()
        self.app_context.pop()
