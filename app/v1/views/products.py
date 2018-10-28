'''Products resource.'''
import re
from flask_restful import Resource, reqparse

from app.v1.models import Product, db
from app.decorators import admin_required

class ProductResource(Resource):
    '''Class for handling products.'''

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help='Name (str) is required.')
    parser.add_argument('price', required=True, type=int, help='Price (int) is required.')

    @admin_required
    def post(cls):
        '''Post Product'''
        arguments = ProductResource.parser.parse_args()
        name = arguments.get('name')
        price = arguments.get('price')

        for product in getattr(db, 'products'):
            if name == product['name']:
                return {'message': 'Product with that name already exists.'}, 409
        if not re.match('^[a-zA-Z 0-9]+$', name):
            return {'message': "Enter a valid product name"}, 400
        product = Product(name=name, price=price)
        product = product.save()
        return {'message': 'Product successfully added.', 'product': product}, 201


    def get(cls, product_id=None):
        '''Get Products'''
        if product_id:
            product = [product for product in getattr(db, 'products') if product['id'] == product_id]
            if product:
                return {'message': 'Product found.', 'product': product}, 200
            return {'message': 'Product not found.'}, 404

        # Get all products
        products = getattr(db, 'products')
        if not products:
            return {'message': 'No products found.'}, 404
        return {'message': 'Products found.', 'PRODUCTS': products}, 200
