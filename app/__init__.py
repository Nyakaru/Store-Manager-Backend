"""Initializes the flask app"""

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from app.v1.views.views_users import NewUsers, GetAllUsers, GetUser, LoginUser
from app.v1.views.views_products import NewProducts, GetProduct
from app.v1.views.views_sales import MakeSale, GetSpecificSale
from app.v1.models.model_users import generate_admin

from config import app_config

def create_app(config_name):
    """Factory initialization for the app"""
    app = Flask(__name__)
    app.config.from_object(app_config["development"])
   
  

    # Initialize flask_restful and add routes
    api_endpoint = Api(app)
    
    # Users Resource
    api_endpoint.add_resource(NewUsers, '/api/v1/auth/signup')
    api_endpoint.add_resource(GetAllUsers, '/api/v1/users')
    api_endpoint.add_resource(GetUser, '/api/v1/users/<int:user_id>')
    api_endpoint.add_resource(LoginUser, '/api/v1/auth/login')

    # Products Resource
    api_endpoint.add_resource(NewProducts, '/api/v1/products')
    api_endpoint.add_resource(GetProduct, '/api/v1/products/<int:product_id>')

    # Sales Resource
    api_endpoint.add_resource(MakeSale, '/api/v1/sales')
    api_endpoint.add_resource(GetSpecificSale, '/api/v1/sales/<int:sale_id>')

    # Initializes flask_jwt_extended
    jwt = JWTManager(app)

    return app

