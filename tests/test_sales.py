'''Test sales.'''
from json import dumps, loads
from .base import BaseCase
from app.models import Sale

SALES_URL = '/api/v1/sales/'
SALE_URL = '/api/v1/sales/1'



class TestsaleResource(BaseCase):
    '''Test sale resources.'''

    def test_can_create_a_sale(self):
        '''Test the POST functionality for a sale.'''
        # Using valid data.
        valid_sale_data = dumps({ "product_dict": {1: 3}})
        response = self.client.post(
            SALES_URL, data=valid_sale_data)
        #Check status code is 201
        self.assertEqual(response.status_code, 201)
        expected = 'Sale has been created successfully.'
        #Check correct message returned.
        self.assertEqual(expected, loads(
        response.data.decode('utf-8'))['message'])
        #Check sale created with invalid product_dict.
        invalid_sale_data = dumps({ 'product_dict': []})
        response = self.client.post(
            SALES_URL, data=invalid_sale_data)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'product_dict (dict) is required.'
        # Check correct message returned.
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        # Create sale for non-existent product.
        valid_sale_data = dumps({ 'product_dict': {2: 3}})
        response = self.client.post(
            SALES_URL, data=valid_sale_data)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Product 2 does not exist.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        # Place sale with invalid quantity.
        valid_sale_data = dumps({ 'product_dict': {1: 'b'}})
        response = self.client.post(
            SALES_URL, data=valid_sale_data)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Product quantities should be integers.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])
        # Place sale with invalid product_id.
        valid_sale_data = dumps({ 'product_dict': {'a': 1}})
        response = self.client.post(
            SALES_URL, data=valid_sale_data)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Product ID should be an integer.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])

    def test_can_get_sale(self):
        

        self.sale2 = Sale( {1: 4})
        self.sale2.save()
        #  Get one.
        response = self.client.get(SALE_URL,)
        self.assertEqual(response.status_code, 200)
        expected = 'Sale record found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertTrue(loads(response.data.decode('utf-8'))['sale'])
        #  Request get all.
        response = self.client.get(SALES_URL,)
        self.assertEqual(response.status_code, 200)
        expected = 'Sales records found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertEqual(
            len(loads(response.data.decode('utf-8'))['sales']) ,2)
        
        # Returns 404 if sale does not exist.
        response = self.client.get('/api/v1/sales/4',)
        self.assertEqual(response.status_code, 404)
        expected = 'Sale record not found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

   