'''Test models.'''

from app.v2.models.product_models import Product
from app.v2.models.user_models import User
from .base import BaseCase


class TestModels(BaseCase):
    '''Class for testing the user model.'''

    def test_user(self):
        '''Test user model.'''

        # Test saving a user.
        self.user1.add_user()
        self.assertEqual(1, len(User.get_all()))

        # Test getting a user.
        self.assertIsInstance(User.get(id=1), tuple)

        # test default role assigned is user
        self.assertEqual(User.get_roles(user_id=1)[0], 'user')
        # Test getting a user by key.
        self.assertIsInstance(User.get(username='user1'), tuple)

        # Test get all users.
        self.assertIsInstance(User.get_all(), list)
        self.assertEqual(1, len(User.get_all()))

        # Test deleting a user.
        self.user1.delete_user(1)
        self.assertEqual(None, User.get(id=1))
        self.assertEqual(0, len(User.get_all()))
        self.assertEqual(None, User.get(username='user1'))

    def test_product(self):
        '''Test Product model.'''
        pass
        self.assertEqual(0, len(Product.get_all()))

        # # Test saving a Product.
        self.product1.add_product()
        self.assertEqual(1, len(Product.get_all()))

        # Test getting a Product.
        self.assertIsInstance(Product.get(id=1), tuple)

        # Test get all Products.
        self.assertIsInstance(Product.get_all(), list)
        self.assertEqual(1, len(Product.get_all()))

        # Test deleting a Product.
        Product.delete(id=1)
        self.assertEqual(None, Product.get(id=1))
        self.assertEqual(0, len(Product.get_all()))

    