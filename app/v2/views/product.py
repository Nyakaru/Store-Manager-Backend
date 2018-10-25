'''Products resource.'''

import re
from json import loads

from flask import request
from flask_restful import Resource, reqparse

from app.v2.models.products_model import Product
from app.v2.decorators import login_required, admin_required


class DBproductResource(Resource):
    '''Class for handling products.'''

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help='Name (str) is required.')
    parser.add_argument('price', required=True, type=int, help='Price (int) is required.')

    @admin_required
    def post(self):
        '''Create a new product.'''
        arguments = DBProductResource.parser.parse_args()
        name = arguments.get('name')
        price = arguments.get('price')
        name_format = re.compile(r"([a-zA-Z0-9])")

        if not re.match(name_format, name):
            return{'message': "Invalid name!"},400

        product_exists = Product.get(name=name)
        if product_exists:
            return {'message': 'Product with that name already exists.'},409
        product = Product(name=name, price=price)
        product.add_product()
        product = Product.get(name=name)
        return {'message': 'Product successfully added.', 'product': product.view(product)}, 201

    @login_required
    def get(self, product_id=None):
        ''' Get product/products.'''
        # Get a single product.
        if product_id:
            product = Product.get(id=product_id)
            if product:
                product = Product.get(id=product_id)
                return {'message': 'Product found.', 'product': Product.view(product=product)}, 200
            return {'message': 'Product not found.'}, 404

        # Get all products
        products = Product.get_all()
        if not products:
            return {'message': 'No products found.'}, 404
        products = [Product.view(product) for product in products]
        return {'products': products}, 200

    @login_required
    @admin_required
    def put(self, product_id):
        ''' Edit a product.'''
        json_data = loads(request.data.decode())
        name = json_data.get('name', None)
        price = json_data.get('price', None)
        new_data = {}
        product = Product.get(id=product_id)

        if name:
            try:
                int(name)
                return {'message': "Invalid name!"}, 400
            except:
                if Product.get(name=name):
                    return {'message': "A product with that name exists!"}, 409
                elif isinstance(name, str):
                    new_data.update({'name': name})
                else:
                    return {'message': 'Name should be a string.'}, 400

        if price:
            if isinstance(price, int):
                new_data.update({'price': price})
            else:
                return {'message': 'Price should be an integer.'}, 400

        if product:
            id = product_id
            Product.update(id=id, new_data=new_data)
            product = Product.get(id=id)
            # product = Product(name=product[1],price=product[2])
            product = Product.view(product)
            return {
                'message': 'Product has been updated successfully.',
                'new_product': product}, 200
        return {'message': 'Product does not exist.'}, 404

    @admin_required
    def delete(self, product_id):
        '''Delete a product.'''
        Product = Product.get(id=Product_id)
        if product:
            Product.delete(product_id)
            return{
                'message': 'Product {} successfully deleted.'.format(product_id)
            }, 200
        return {'message': 'Product does not exist'}, 404
