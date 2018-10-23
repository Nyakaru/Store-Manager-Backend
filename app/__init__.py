'''Create app'''

from flask import Flask
from flask_restful import Api

from config import configurations
from app.v1.views.products import ProductResource
from app.v1.views.sales import SaleResource
from app.v1.views.user import UserResource
from app.v1.views.auth import AuthResource

def create_app():
    '''Create the flask app.'''
    app = Flask(__name__)
    app.config.from_object(configurations["development"])
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
    api.add_resource(
        ProductResource, '/api/v1/products', '/api/v1/products/<int:product_id>')
    api.add_resource(
        SaleResource, '/api/v1/sales', '/api/v1/sales/<int:sale_id>')
    api.add_resource(
        UserResource, '/api/v1/users/signup')
    api.add_resource(
        AuthResource, '/api/v1/users/signin')
    return app
    