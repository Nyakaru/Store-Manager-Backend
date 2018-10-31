'''Test sales.'''
from json import dumps, loads
from .base import BaseCase
from app.v2.models.user_models import User
from app.v2.models.sale_models import Sale

SALES_URL = '/api/v2/sales/'
SALE_URL = '/api/v2/sales/1'


class TestSaleResource(BaseCase):
    '''Test sales resources.'''

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
        # Create sales for non-existent product.
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
        # Place sales with invalid quantity.
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
        # Place sales with invalid product_id.
        valid_sale_data = dumps({'product_dict': {'a': 1}})
        response = self.client.post(
            SALES_URL, data=valid_sale_data, headers=headers)
        # Check status code is 400.
        self.assertEqual(response.status_code, 400)
        expected = 'Product ID should be an integer.'
        self.assertEqual(expected, loads(
            response.data.decode('utf-8'))['message'])

    def test_can_get_sales(self):
        self.product1.add_product()
        user_token = self.get_user_token()
        self.sale1.add_sale()
        user_header = {'Authorization': 'Bearer {}'.format(user_token)}
        # Add an extra user.
        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.add_user()
        self.sale2 = Sale(2, {1: 4})
        self.sale2.add_sale()
        token = self.get_admin_token()
        user2_header = {'Authorization': 'Bearer {}'.format(token)}

        # User request get one.
        response = self.client.get(SALE_URL, headers=user2_header)
        self.assertEqual(response.status_code, 200)
        expected = 'Sale found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_user1_cannot_view_user2_sales(self):
        self.product1.add_product()
        user_token = self.get_user_token()
        self.sale1.add_sale()
        user_header = {'Authorization': 'Bearer {}'.format(user_token)}
        # Add an extra user.
        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.add_user()
        self.sale2 = Sale(2, {1: 4})
        self.sale2.add_sale()
        token = self.get_admin_token()
        user2_header = {'Authorization': 'Bearer {}'.format(token)}
        response = self.client.get('/api/v2/sales/2', headers=user_header)
        self.assertEqual(response.status_code, 403)
        expected = 'You do not have permission to see this sale.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
    
    def test_non_existent_sale(self):
        # Returns 404 if sales does not exist.
        user_token = self.get_user_token()
        user_header = {'Authorization': 'Bearer {}'.format(user_token)}
        response = self.client.get('/api/v2/sales/4', headers=user_header)
        self.assertEqual(response.status_code, 404)
        expected = 'Sale not found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)

    def test_user_can_only_get_their_sale(self):
        self.user1.add_user()
        self.product1.add_product()
        self.sale1.add_sale()
        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.add_user()
        token = self.user2.generate_token(id=2)
        sale = Sale(2, {1: 4})
        sale.add_sale()

        user2_token = {'Authorization': 'Bearer {}'.format(
            token)}

        # User request get all.
        response = self.client.get(SALES_URL, headers=user2_token)

        self.assertEqual(response.status_code, 200)
        expected = 'Sales found.'
        sales = loads(response.data.decode('utf-8'))['sales']
        self.assertEqual(loads(response.data.decode('utf-8'))['message']
                         , expected)
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0]['sale_id'], 2)

    def test_admin_can_get_all_sales(self):
        self.product1.add_product()
        self.user1.add_user()
        self.sale1.add_sale()
        self.user2 = User(
            username='user2', email='user2@email.com', password='pass#123')
        self.user2.add_user()
        self.sale2 = Sale(2, {1: 4})
        self.sale2.add_sale()

        # Admin request.
        admin_token = self.get_admin_token()
        admin_header = {'Authorization': 'Bearer {}'.format(admin_token)}
        response = self.client.get(SALES_URL, headers=admin_header)
        self.assertEqual(response.status_code, 200)
        expected = 'Sales found.'
        self.assertEqual(loads(response.data.decode('utf-8'))
                         ['message'], expected)
        self.assertEqual(
            len(loads(response.data.decode('utf-8'))['sales']), 2)