'''Base test class.'''
from unittest import TestCase
import psycopg2 

from app.v2.models.product_models import Product
from app.v2.models.user_models import User
from app.v2.connect_db import create, connect_to_db
from app import create_app


class BaseCase(TestCase):
    '''Base class to be inherited by all other testcases.'''

    def setUp(self):
        '''Set up test application.'''
        create('testing')
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user1 = User(
            username='user1',
            email='user1@email.com',
            password='pass#123')
        self.product1 = Product(
            name='Product1',
            price=100
        )
        self.product1.save()
        
        self.user_data_1 = {
            'username': 'user3',
            'email': 'user3@mail.com',
            'password': 'password',
            'confirm_password': 'password'
        }

        self.user_data_2 = {
            'username': '',
            'email': 'user2@mail.com',
            'password': 'password',
            'confirm_password': 'password'
        }

        self.user_data_3 = {
            'username': 'user3',
            'email': 'user3mail.com',
            'password': 'password',
            'confirm_password': 'password'
        }

        self.valid_product_data = {
            'name': 'Product2',
            'price': 100
        }
        self.valid_product_data2 = {
            'name': 'Product3',
            'price': 100
        }
        self.invalid_product_data = {
            'name': None,
            'price': None
        }

    def get_user_token(self):
        '''Create a token for testing.'''
        self.user1.add_user()
        return self.user1.generate_token(id=1)

    def get_admin_token(self):
        '''Create an admin token for testing.'''

        admin = User(
            username='admin', password='pass1234', email='admin@mail.com')
        admin.add_user()
        admin_id = User.get(username='admin')[0]
        admin.assign_user_a_role('admin', admin_id)

        return admin.generate_token(id=admin_id)

    def get_super_user_token(self):
        superuser = User(username='Administrator',
                         password='pass400&', email='admin@admin.com')
        superuser.add_user()
        superuser_id = User.get(username='Administrator')[0]
        superuser.assign_user_a_role('superuser',superuser_id)

        return superuser.generate_token(id=superuser_id)

    def tearDown(self):
        '''Delete database and recreate it with no data.'''

        conn = connect_to_db('testing')
        cur = conn.cursor()
        cur.execute("""DROP TABLE IF EXISTS users CASCADE;""")
        cur.execute(  """DROP TABLE IF EXISTS  products CASCADE;""")
        cur.execute(  """DROP TABLE IF EXISTS  roles CASCADE;""")
        cur.execute(  """DROP TABLE IF EXISTS user_roles CASCADE;""")
        conn.commit()
        conn.close()
        