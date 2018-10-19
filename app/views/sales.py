'''sale resource.'''
from flask import request
from flask_restful import Resource

from app.models import Product, Sale

class SaleResource(Resource):
    '''Class for handling sales.'''

    @classmethod
    def post(cls):
        '''Create an sale.'''

        data = request.get_json(force=True)

        product_dict = data.get('product_dict')

        if not isinstance(product_dict, dict):
            return {'message': 'product_dict (dict) is required.'}, 400

        # Check if product being sold exists.
        product_ids = product_dict.keys()
        for product_id in product_ids:
            try:
                product_id = int(product_id)
                product = Product.get_by_key(id=int(product_id))
                if product:
                    if not isinstance(product_dict[str(product_id)], int):
                        return {
                            'message': 'Product quantities should be integers.'
                        }, 400
                else:
                    return {
                        'message': 'Product {} does not exist.'.format(product_id)
                    }, 400
            except ValueError:
                return {'message': 'Product ID should be an integer.'}, 400
        sale = Sale(products_dict=product_dict)
        sale = sale.save()
        return {
            'message': 'Sale has been created successfully.', 'sale': sale
        }, 201
    @classmethod
    def get(cls, sale_id=None):
        '''Get sales.'''

        if sale_id:
            sale = Sale.get(id=sale_id)
            if sale:
                return {'message': 'Sale record found.', 'sale': sale.view()}, 200

            return {'message': 'Sale record not found.'}, 404

        sales = Sale.get_all()
        sales = [sales[sale].view() for sale in sales]
        if sales:
            return {'message': 'Sales records found.', 'sales': sales}, 200
        return {'message': 'Sales records not found.'}, 404
