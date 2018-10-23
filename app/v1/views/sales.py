import re
from flask_restful import Resource, reqparse

from app.v1.models import Product, db ,Sale
from app.v1.decorators import login_required, admin_required

class SaleResource(Resource):
    '''Class for handling products.'''

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help='Name (str) is required.')
    parser.add_argument('price', required=True, type=int, help='Price (int) is required.')

    @login_required
    def post(cls):
            '''Post Product'''
            arguments = SaleResource.parser.parse_args()
            name = arguments.get('name')
            price = arguments.get('price')

            for product in getattr(db, 'products'):
                if not name == product['name']:
                    return {'message': 'Product does not exist.'}, 400
            if not re.match('^[a-zA-Z 0-9]+$', name):
                return {'message': "Enter a valid sale name"}, 400
            sale = Sale(name=name, price=price)
            sale = sale.save()
            return {'message': 'Sale has successfully been added.', 'sale': sale}, 201

    
    def get(cls, sale_id=None):
        '''Get Products'''
        if sale_id:
            sale = [sale for sale in getattr(db,'sales') if sale['id'] == sale_id]
            if sale:
                return {'message': 'Sale record found.', 'sale': sale}, 200
            return {'message': 'Sale record not found.'}, 404

        # Get all products
        sales = getattr(db,'sales')
        if not sales:
            return {'message': 'No sales records found.'}, 404
        return {'message': 'Sale records found.', 'SALES': sales}, 200



