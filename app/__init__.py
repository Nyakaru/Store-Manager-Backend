'''Create app'''

from flask import Flask
from flask_restful import Api

from config import configurations
from app.v1.views.products import ProductResource
from app.v1.views.sales import SaleResource
from app.v1.views.user import UserResource
from app.v1.views.auth import AuthResource

from app.v2.views.users import DBUserResource
from app.v2.views.auth import DBAuthResource
from app.v2.views.product import DBProductResource
from app.v2.views.manage_user import DBManageUsersResource



def create_app(configuration):
    '''Create the flask app.'''
    app = Flask(__name__)
    app.config.from_object(configurations[configuration])
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

    # v2 urls
    api.add_resource(
        DBUserResource, '/api/v2/users/signup')
    api.add_resource(
        DBAuthResource, '/api/v2/users/signin')
    api.add_resource(
        DBProductResource, '/api/v2/products', '/api/v2/products/<int:product_id>')
    api.add_resource(
        DBManageUsersResource, '/api/v2/users/manage/<int:user_id>')

    return app
    