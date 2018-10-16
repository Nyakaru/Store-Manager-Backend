'''Create app'''

from flask import Flask
from flask_restful import Api

from .config import configurations
from app.views.products import ProductResource



def create_app(configuration):
    '''Create the flask app.'''
    
    app = Flask(__name__)
    app.config.from_object(configurations["development"])
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
    

    api.add_resource(
        ProductResource, '/api/v1/products', '/api/v1/products/<int:product_id>')
    
    
    return app

    