'''Test models.'''

from app.models import Product, Sale
from .base import BaseCase





class TestModels(BaseCase):
    '''Class for testing the models.'''

    def test_products(self):
        '''Test product model.'''

        # Test saving a product.
        result = self.product1.save()
        expected = {'price': 100.0, 'id': 1, 'name': 'Product1'}
        self.assertDictEqual(result, expected)

        # Test getting a product.
        self.assertIsInstance(Product.get(id=1), Product)

        # Test get all Products.
        self.assertIsInstance(Product.get_all(), dict)
        self.assertEqual(1, len(Product.get_all()))

    def test_sales(self):
        '''Test sale model.'''

        # Test saving a sale
        result = sorted(list(self.sale1.save().keys()))
        expected = sorted([ 'id','products', 'total'])
        self.assertEqual(result, expected)

        # Test getting a Sale.
        self.assertIsInstance(Sale.get(id=1), Sale)

        # Test get all Sales.
        self.assertIsInstance(Sale.get_all(), dict)
        self.assertEqual(1, len(Sale.get_all()))


        

        