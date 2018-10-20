from datetime import timedelta
from hashlib import sha256
from os import getenv
from time import time
import jwt

from jwt import encode, decode
'''Models and their methods.'''

class DB():
    '''In memory database.'''

    def __init__(self):
        '''Create an empty database.'''

        self.users = {}
        self.products = {}
        self.sales = {}

    def drop(self):
        '''Drop entire database.'''

        self.__init__()


db = DB()


class Base():
    '''Base class to be inherited by other models.'''

    def save(self):
        '''Add object to database.'''

        if self.id is None:
            setattr(self, 'id', len(getattr(db, self.tablename)) + 1)
        getattr(db, self.tablename).update({self.id: self})
        return self.view()

    def update(self, new_data):
        '''Update object.'''

        keys = new_data.keys()
        for key in keys:
            setattr(self, key, new_data[key])
        return self.save()

    def view(self):
        '''View object as a dictionary.'''

        return self.__dict__

    @classmethod
    def get(cls, id):
        '''Get object from it's table by id.'''

        return getattr(db, cls.tablename).get(id)

    @classmethod
    def get_all(cls):
        '''Get all objects in a table.'''

        return getattr(db, cls.tablename)
    @classmethod
    def get_by_key(cls, **kwargs):
        '''Get an object by a key that is not id.'''

        kwarg = list(kwargs.keys())[0]
        db_store = getattr(db, cls.tablename)
        for key in db_store:
            obj = db_store[key]
            if obj.view()[kwarg] == kwargs[kwarg]:
                return obj
        return None

class Product(Base):
    '''Product model.'''

    tablename = 'products'

    def __init__(self, name, price):
        '''Initialize a product.'''

        self.id = None
        self.name = name
        self.price = price



class Sale(Base):
    '''Sales model.'''
    tablename = 'sales'

    def __init__(self, products_dict):
        '''Initialize a sale.'''
        self.id = None
        self.products = [
            {'quantity': products_dict[product_id],
             'product': Product.get(id=int(product_id)).view()}
            for product_id in products_dict.keys()]
        self.total = self.get_total()

    def get_total(self):
        '''Get total cost of a sale.'''
        return sum([i['quantity'] * i['product']['price'] for i in self.products])
class User(Base):
    '''User model.'''

    tablename = 'users'

    def __init__(self, username, password, email):
        '''Initialize a user.'''

        self.id = None
        self.username = username
        self.email = email
        self.password = self.make_hash(password)
        self.roles = []

    def make_hash(self, password):
        '''Generate hash of password.'''

        return sha256(password.encode('utf-8')).hexdigest()

    def generate_token(self):
        '''Create a token for a user.'''

        key = getenv('APP_SECRET_KEY')
        payload = {
            'user_id': self.id,
            'username': self.username,
            'roles': self.roles,
            'created_at': time(),
            'exp': time() + timedelta(hours=7).total_seconds()}
        return jwt.encode(
            payload=payload, key=str(key), algorithm='HS256').decode('utf-8')

    @staticmethod
    def decode_token(token):
        '''View information inside a token.'''

        key = getenv('APP_SECRET_KEY')
        return jwt.decode(token, key=str(key))

    def check_password(self, password):
        '''Validate a user's password.'''

        return True if self.make_hash(password) == self.password else False

    def view(self):
        '''View a user's information.'''

        return {
            'username': self.username,
            'email': self.email,
            'roles': self.roles,
            'id': self.id
        }