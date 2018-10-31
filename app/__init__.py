'''Create app'''

from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS

from config import configurations
from app.v1.views.products import ProductResource
from app.v1.views.sales import SaleResource
from app.v1.views.user import UserResource
from app.v1.views.auth import AuthResource

from app.v2.views.users import DBUserResource
from app.v2.views.auth import DBAuthResource
from app.v2.views.product import DBProductResource
from app.v2.views.manage_user import DBManageUsersResource
from app.v2.views.sale import DBSaleResource

def create_app(configuration):
    '''Create the flask app.'''
    app = Flask(__name__)
    api_blueprint = Blueprint('api', __name__)
    api = Api(api_blueprint)
    app.config.from_object(configurations[configuration])
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()

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
        DBSaleResource, '/api/v2/sales/', '/api/v2/sales/<int:sale_id>')
    api.add_resource(
        DBManageUsersResource, '/api/v2/users/manage/<int:user_id>')

    app.register_blueprint(api_blueprint)

    cors = CORS(app, resources={r'/api/*': {'origins': '*'}},
                supports_credentials=True)
    return app
