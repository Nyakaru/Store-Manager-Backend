from flask import request
from flask_restful import Resource

from app.v2.models.product_models import Product
from app.v2.models.sale_models import Sale
from app.v2.models.user_models import User
from app.v2.decorators import login_required, admin_required


class DBSaleResource(Resource):
    '''Class for handling sales.'''

    @login_required
    def post(self):
        '''Create an sale.'''
        data = request.get_json(force=True)
        product_dict = data.get('product_dict')

        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(' ')[1]
        payload = User.decode_token(token=access_token)
        user_id = payload['user_id']

        if not isinstance(user_id, int):
            return {'message': 'User_id (int) is required.'}, 400
        if not isinstance(product_dict, dict):
            return {'message': 'Product_dict (dict) is required.'}, 400
        if product_dict is None: 
            return{'message': "You haven't selected any products"},200

        # Check if product sold exists.
        product_ids = product_dict.keys()
        for product_id in product_ids:
            try:
                product_id = int(product_id)
                product =Product.get(id=int(product_id))
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

        sale =Sale(user_id=user_id, product_dict=product_dict)
        sale_id = sale.add_sale()

        return {
            'message': 'Sale has been created successfully.',
            'sale_id': sale_id,
            'products': Sale.get_products(sale_id)
        }, 201

    @login_required
    def get(self, sale_id=None):
        '''Get sales.'''
        authorization_header = request.headers.get('Authorization')
        access_token = authorization_header.split(' ')[1]
        payload = User.decode_token(token=access_token)
        roles, user_id = payload['roles'], payload['user_id']
        is_admin = 'admin' in roles
        if sale_id:
            sale = Sale.get(id=sale_id)
            if sale is None:
                return {'message': 'Sale not found.'}, 404
            if sale[1] == user_id or is_admin:
                return {'message': 'Sale found.', 'sale': Sale.view(sale)}, 200
            else:
                return {
                    'message': 'You do not have permission to see this sale.'
                }, 403
        else:
            if is_admin:
                sales = Sale.get_all()
                sales = [Sale.view(sale) for sale in sales]
                return {'message': "Sales found.", 'sales': sales},200
            else:
                sales = Sale.get_all_by_user_id(user_id=user_id)
                if len(sales) == 0:
                    return {'message': 'Sales not found'}, 404
                sales = [Sale.view(sale) for sale in sales]
                return {'message': 'Sales found.', 'sales': sales}, 200

