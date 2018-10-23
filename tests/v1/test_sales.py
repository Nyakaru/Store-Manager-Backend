'''Tests product resource.'''
from json import loads, dumps
from .base import BaseCase

SALES_URL = '/api/v1/sales/'
SALE_URL = '/api/v1/sales/1'
PRODUCTS_URL = '/api/v1/products/'


class TestsaleResource(BaseCase):
    '''Class to test products'''
    def test_attendant_create_sale(self):
        '''Test the POST functionality for a product.'''
        # Get admin token.

        token = self.get_attendant_token()
        self.headers['Authorization'] = token
        response = self.client.post(SALES_URL, data=dumps(self.valid_product_data), headers=self.headers)
        expected = 'Sale has successfully been added.'
        self.assertEqual(response.json.get('message'), expected)
        self.assertEqual(response.status_code, 201)
    
    def test_can_admin_cannot_create_sale(self):
        '''Test the POST functionality for a product.'''
        token = self.get_admin_token()
        self.headers['Authorization'] = token
        response = self.client.post(SALES_URL, data=dumps(self.valid_product_data), headers=self.headers)
        expected = 'This action requires an attendant token.'
        self.assertEqual(response.json.get('message'), expected)
        self.assertEqual(response.status_code, 400)

    def test_can_cannot_create_sale(self):
        '''Test the POST functionality for a product.'''
        response = self.client.post(SALES_URL, data=dumps(self.valid_product_data), headers=self.headers)
        expected = 'please provide a token'
        self.assertEqual(response.json.get('message'), expected)
        self.assertEqual(response.status_code, 400)
    
    def test_empty_name_sale(self):
        # Using empty name.
        token = self.get_attendant_token()
        self.headers['Authorization'] = token
        response = self.client.post(SALES_URL, data=dumps(self.invalid_product_name), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Enter a valid sale name'
        self.assertEqual(response.json['message'], expected)
    
    def test_invalid_saleprice(self):
        # Provide an invalid sale price.
        token = self.get_attendant_token()
        self.headers['Authorization'] = token
        response = self.client.post(SALES_URL, data=dumps(self.invalid_product_price_data), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Price (int) is required.'
        self.assertEqual(response.json['message']['price'], expected)

    def test_can_get_all_sales(self):
        # Test getting all products.
        token = self.get_attendant_token()
        self.headers['Authorization'] = token
        response = self.client.post(SALES_URL, data=dumps(self.valid_product_data), headers=self.headers)
        response = self.client.get(SALES_URL)
        self.assertEqual(response.status_code, 200)
        expected = 'Sale records found.'
        self.assertEqual(response.json['message'], expected)
    
    def test_can_get_single_sale(self):
        #Test getting single product.
        token = self.get_attendant_token()
        self.headers['Authorization'] = token
        response = self.client.post(SALES_URL, data=dumps(self.valid_product_data), headers=self.headers)
        response = self.client.get(SALE_URL)
        self.assertEqual(response.status_code, 200)
        expected = 'Sale record found.'
        self.assertEqual(response.json['message'], expected)
    
    
    def test_non_existent_product(self):
        # Test returns 404 for non-existent product.
        token = self.get_attendant_token()
        self.headers['Authorization'] = token
        response = self.client.get('/api/v1/sales/4')
        self.assertEqual(response.status_code, 404)
        expected = 'Sale record not found.'
        self.assertEqual(response.json['message'], expected)
