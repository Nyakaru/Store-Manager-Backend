"""Views for the sales resource"""
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.v1.models.model_sales import Sales

class MakeSale(Resource):
    """
    Class to handle creating sales
    POST /api/v1/sales -> Creates a new sale record
    GET /api/v1/sales -> Fetch all sales records
    """

    @jwt_required
    def post(self):
        """Route to handle creating a new sale"""
        # Gets user info from the token
        current_user = get_jwt_identity()

        # Checks if the user is an admin
        if current_user['admin'] == True:
            return {'msg':'Sorry, this route is not accessible to admins'}, 403

        return Sales().make_sale(
            request.json['product'],
            request.json['quantity'],
            request.json['price'])
    
    @jwt_required
    def get(self):
        """Route to handle getting all sales"""
        # Gets user info from the token
        current_user = get_jwt_identity()

        # Checks if the user is an attendant
        if current_user['admin'] == False:
            return {'msg':'Sorry, this route is only accessible to admins'}, 403
        return Sales().get_all_sales()
    
class GetSpecificSale(Resource):
    """
    Class to fetch a specific record
    GET /api/v1/sales/<int:sale_id> -> Fetch a specific sale record
    """
    @jwt_required
    def get(self, sale_id):
        """Route to handle fetching a specific record"""
        return Sales().get_one_sale(sale_id)

