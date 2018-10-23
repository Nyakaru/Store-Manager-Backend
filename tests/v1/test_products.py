'''Tests product resource.'''
from json import loads, dumps
from .base import BaseCase

PRODUCTS_URL = '/api/v1/products/'
PRODUCT_URL = '/api/v1/products/1'


class TestproductResource(BaseCase):
    '''Class to test products'''
    def test_can_admin_create_a_product(self):
        '''Test the POST functionality for a product.'''
        # Get admin token.
        token = self.get_admin_token()
        self.headers['Authorization'] = token
        response = self.client.post(PRODUCTS_URL, data=dumps(self.valid_product_data), headers=self.headers)
        expected = 'Product successfully added.'
        self.assertEqual(response.json.get('message'), expected)
        self.assertEqual(response.status_code, 201)
    
    def test_can_duplicate_product(self):
        #Using duplicate product.
        token = self.get_admin_token()
        self.headers['Authorization'] = token
        response = self.client.post(PRODUCTS_URL, data=dumps(self.valid_product_data), headers=self.headers)
        response = self.client.post(PRODUCTS_URL, data=dumps(self.valid_product_data), headers=self.headers)
        self.assertEqual(response.status_code, 409)
        expected = 'Product with that name already exists.'
        self.assertEqual(response.json['message'], expected)
    
    def test_empty_name_product(self):
        # Using empty name.
        token = self.get_admin_token()
        self.headers['Authorization'] = token
        response = self.client.post(PRODUCTS_URL, data=dumps(self.invalid_product_name), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Enter a valid product name'
        self.assertEqual(response.json['message'], expected)
    
    def test_invalid_price(self):
        # Provide an invalid product price.
        token = self.get_admin_token()
        self.headers['Authorization'] = token
        response = self.client.post(PRODUCTS_URL, data=dumps(self.invalid_product_price_data), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Price (int) is required.'
        self.assertEqual(response.json['message']['price'], expected)

    def test_can_get_all_products(self):
        '''Test GET functionality of products.'''
        # Test getting all products.
        token = self.get_admin_token()
        self.headers['Authorization'] = token
        response = self.client.post(PRODUCTS_URL, data=dumps(self.valid_product_data), headers=self.headers)
        response = self.client.get(PRODUCTS_URL)
        self.assertEqual(response.status_code, 200)
        expected = 'Products found.'
        self.assertEqual(response.json['message'], expected)
    
    def test_can_get_single_product(self):
        #Test getting single product.
        token = self.get_admin_token()
        self.headers['Authorization'] = token
        response = self.client.post(PRODUCTS_URL, data=dumps(self.valid_product_data), headers=self.headers)
        response = self.client.get(PRODUCT_URL)
        self.assertEqual(response.status_code, 200)
        expected = 'Product found.'
        self.assertEqual(response.json['message'], expected)
    
    def test_non_existent_product(self):
        # Test returns 404 for non-existent product.
        response = self.client.get('/api/v1/products/4')
        self.assertEqual(response.status_code, 404)
        expected = 'Product not found.'
        self.assertEqual(response.json['message'], expected)

    def test_attendant_cannot_create_product(self):
        '''ahjdhksdlfsf'''
        token = self.get_attendant_token()
        self.headers['Authorization'] = token
        response = self.client.post(PRODUCTS_URL, data=dumps(self.valid_product_data), headers=self.headers)
        expected = 'This action requires an admin token.'
        self.assertEqual(response.json.get('message'), expected)
        self.assertEqual(response.status_code, 403)
