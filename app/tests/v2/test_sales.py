'''Test orders.'''
from json import dumps, loads
from .base import BaseCase
from app.v2.models.user_models import User
from app.v2.models.sale_models import Sale

SALES_URL = '/api/v2/sales/'
SALE_URL = '/api/v2/sales/1'


class TestSaleResource(BaseCase):
    '''Test order resources.'''

    def test_can_create_a_sale(self):
        '''Test the POST functionality for a sale.'''
        self.user1.add_user()
        self.product1.add_product()

        # Request data.
        valid_sale_data = dumps({"product_dict": {1: 3}})
        # Get user token to create header.
        token = self.user1.generate_token(id=1)
        headers = {'Authorization': 'Bearer {}'.format(token)}
        # Using valid data.
        response = self.client.post(
            SALES_URL, data=valid_sale_data, headers=headers)
        # Check status code is 201
        self.assertEqual(response.status_code, 201)
        expected = 'Sale has been created successfully.'
        # Check correct message returned.
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        
    def test_empty_product(self):
        self.user1.add_user()
        token = self.user1.generate_token(id=1)
        headers = {'Authorization': 'Bearer {}'.format(token)}
        invalid_sale_data = dumps({'product_dict': []})
        response = self.client.post(
            SALES_URL, data=invalid_sale_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Product_dict (dict) is required.'
        # Check correct message returned.
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])

    def test_non_existent_product(self):
        self.user1.add_user()
        token = self.user1.generate_token(id=1)
        headers = {'Authorization': 'Bearer {}'.format(token)}
        # Create order for non-existent product.
        valid_sale_data = dumps({'product_dict': {2: 3}})
        response = self.client.post(
            SALES_URL, data=valid_sale_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Product 2 does not exist.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])

    def test_invalid_quantity(self):
        self.user1.add_user()
        self.product1.add_product()
        token = self.user1.generate_token(id=1)
        headers = {'Authorization': 'Bearer {}'.format(token)}
        # Place order with invalid quantity.
        valid_sale_data = dumps({'product_dict': {1: 'b'}})
        response = self.client.post(
            SALES_URL, data=valid_sale_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Product quantities should be integers.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])

    def test_invalid_product_id(self):
        self.user1.add_user()
        token = self.user1.generate_token(id=1)
        headers = {'Authorization': 'Bearer {}'.format(token)}
        # Place order with invalid product_id.
        valid_sale_data = dumps({'product_dict': {'a': 1}})
        response = self.client.post(
            SALES_URL, data=valid_sale_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Product ID should be an integer.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])