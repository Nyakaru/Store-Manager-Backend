'''Products resource.'''
import re
from flask_restful import Resource, reqparse

from app.models import Product
from app.decorators import login_required, admin_required

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

        product_exists = Product.get_by_key(name=name)
        if product_exists:
            return {'message': 'Product with that name already exists.'}, 409
        product = Product(name=name, price=price)
        product = product.save()
        if not re.match('^[a-zA-Z 0-9]+$', name):
            return {'message': "Enter a valid product name"}, 400

        return {'message': 'Product successfully added.', 'product': product}, 201


    def get(cls, product_id=None):
        '''Get Products'''
        if product_id:
            product = Product.get_by_key(id=product_id)
            if product:
                return {'message': 'Product found.', 'product': product.view()}, 200
            return {'message': 'Product not found.'}, 404

        # Get all products
        products = Product.get_all()
        if not products:
            return {'message': 'No products found.'}, 404
        products = [products[key].view() for key in products]
        return {'products': products}, 200
