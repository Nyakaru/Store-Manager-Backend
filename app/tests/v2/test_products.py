'''Tests product resource.'''


from json import loads, dumps
from .base import BaseCase

Products_URL = '/api/v2/products/'
Product_URL = '/api/v2/products/1'


class TestproductResource(BaseCase):
    '''Test the product resources.'''

    def test_can_create_a_product(self):
        '''Test the POST functionality for a product.'''
        # Get admin token.
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        # Using valid data.
        response = self.client.post(
            Products_URL, data=self.valid_product_data, headers=headers)
        self.assertEqual(response.status_code, 201)
        expected = 'Product successfully added.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
    
    def test_duplicate_product(self):
        # Using duplicate product.
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            Products_URL, data=self.valid_product_data, headers=headers)
        response = self.client.post(
            Products_URL, data=self.valid_product_data, headers=headers)
        self.assertEqual(response.status_code, 409)
        expected = 'Product with that name already exists.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
    
    def test_invalid_product_name(self):
        #Using invalid name
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            Products_URL, data={'name':"@lop",'price':600}, headers=headers)
        self.assertEqual(400,response.status_code)

    def test_invalid_data(self):
        # Using invalid data.
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            Products_URL, data=self.invalid_product_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Name (str) is required.'
        self.assertEqual(
            loads(response.data.decode('utf-8'))['message']['name'], expected)

    def test_invalid_price(self):
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        self.invalid_product_data.update({'name': 'product 1'})
        response = self.client.post(
            Products_URL, data=self.invalid_product_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Price (int) is required.'
        self.assertEqual(
            loads(response.data.decode('utf-8'))['message']['price'], expected)

    def test_only_admin_can_create_a_product(self):
        # Test only an admin can create a product.
        token = self.get_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.post(
            Products_URL, data=self.valid_product_data2, headers=headers)
        self.assertEqual(response.status_code, 403)
        expected = 'This action requires an admin token.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_token_required_to_create_product(self):
        # Test invalid headers.
        response = self.client.post(
            Products_URL, data=self.valid_product_data,
            headers={})
        self.assertEqual(response.status_code, 400)
        expected = 'Ensure you have an authorization header.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_can_get_all_products(self):
        '''Test GET functionality of products.'''
        self.product1.add_product()
        # Test getting all products.
        response = self.client.get(Products_URL)
        self.assertEqual(response.status_code, 200)

        
    def test_can_get_single_product(self):
        # Test getting single product.
        self.product1.add_product()
        response = self.client.get(Product_URL)
        self.assertEqual(response.status_code, 200)
        expected = 'Product found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_non_existent_product(self):
        # Test returns 404 for non-existent product.
        response = self.client.get('/api/v2/products/4')
        self.assertEqual(response.status_code, 404)
        expected = 'Product not found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_can_edit_product(self):
        '''Test editing of products.'''
        self.product1.add_product()
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        #  edit product
        response = self.client.put(
            Product_URL, data=dumps({'name': 'newproduct'}), headers=headers)
        # self.assertEqual(response.status_code, 200)
        expected = 'Product has been updated successfully.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_invalid_edit_product(self):

        # invalid data
        self.product1.add_product()
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.put(
            Product_URL, data=dumps({'name':12}), headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = 'Invalid name!'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_only_admin_can_edit_product(self):
        '''Test protection of products.'''
        self.product1.add_product()
        token = self.get_user_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        #  edit product
        response = self.client.put(
            Product_URL, data=dumps({'name': 'new product'}), headers=headers)
        self.assertEqual(response.status_code, 403)
        expected = 'This action requires an admin token.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)


    def test_can_delete_product(self):
        '''Test deletion of products.'''
        self.product1.add_product()
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.delete(Product_URL, headers=headers)
        self.assertEqual(
            loads(response.data.decode('utf-8'))['message'], 'Product 1 successfully deleted.')

    def test_deleting_non_existent(self):
        self.product1.add_product()
        token = self.get_admin_token()
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.delete(
            '/api/v2/products/10', headers=headers)
        self.assertEqual(
            loads(response.data.decode('utf-8'))['message'], 'Product does not exist')
