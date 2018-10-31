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
