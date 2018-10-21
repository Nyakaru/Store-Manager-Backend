"""Views for the Products Resource"""
from flask_restful import Resource
from flask import request

from app.v1.models.model_products import Products

class NewProducts(Resource):
    """
    Class to handle adding and fetching all products
    POST /api/v1/products -> Creates a new product
    GET /api/v1/products -> Gets all products
    """
    def post(self):
        """Route to handle creating products"""
        return Products().add_product(
            request.json['name'],
            request.json['quantity'],
            request.json['price'],
            request.json['reorder'])
    
    def get(self):
        """Route to fetch all products"""
        return Products().get_all_products()
    
class GetProduct(Resource):
    """
    Class to handle fetching a specific product
    GET /api/v1/products/<int:product_id> -> Fetches a specific product 
    """
    def get(self, product_id):
        """Route to fetch a specific product"""
        return Products().get_one_product(product_id)

