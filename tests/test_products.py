'''Tests product resource.'''
from json import loads
from .base import BaseCase

PRODUCTS_URL = '/api/v1/products/'
PRODUCT_URL = '/api/v1/products/1'


class TestproductResource(BaseCase):
    '''Class to test products'''
    def test_can_create_a_product(self):
        '''Test the POST functionality for a product.'''
        # Get admin token.
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
    
        response = self.client.post(
            PRODUCTS_URL, data=self.valid_product_data)
        self.assertEqual(response.status_code, 201)
        expected = 'Product successfully added.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Using duplicate product.
        response = self.client.post(
            PRODUCTS_URL, data=self.valid_product_data)
        self.assertEqual(response.status_code, 409)
        expected = 'Product with that name already exists.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        # Using empty name.
        response = self.client.post(
            PRODUCTS_URL, data=self.invalid_product_data_name)
        self.assertEqual(response.status_code, 400)
        expected = 'Enter a valid product name'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

        # Using invalid data.
        response = self.client.post(
            PRODUCTS_URL, data=self.invalid_product_data)
        self.assertEqual(response.status_code, 400)
        expected = 'Name (str) is required.'
        self.assertEqual(
            loads(response.data.decode('utf-8'))['message']['name'], expected)
        # Provide a valid product name and try it again.
        self.invalid_product_data.update({'name': 'Product 1'})
        response = self.client.post(
            PRODUCTS_URL, data=self.invalid_product_data)
        self.assertEqual(response.status_code, 400)
        expected = 'Price (int) is required.'
        self.assertEqual(
            loads(response.data.decode('utf-8'))['message']['price'], expected)

    def test_can_get_products(self):
        '''Test GET functionality of products.'''

        # Test getting all products.
        response = self.client.get(PRODUCTS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(loads(response.data.decode('utf-8'))['products'])

        # Test getting single product.
        response = self.client.get(PRODUCT_URL)
        self.assertEqual(response.status_code, 200)
        expected = 'Product found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertTrue(loads(response.data.decode('utf-8'))['product'])

        # Test returns 404 for non-existent product.
        response = self.client.get('/api/v1/products/4')
        self.assertEqual(response.status_code, 404)
        expected = 'Product not found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
