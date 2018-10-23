'''Models and their methods.'''

from hashlib import sha256
from os import getenv

import jwt


class DB():
    '''In memory database.'''

    def __init__(self):
        '''Create an empty database.'''

        self.users = []
        self.products = []
        self.sales = []

    def drop(self):
        '''Drop entire database.'''

        self.__init__()


db = DB()



class Base():
    '''Base class to be inherited by other models.'''

    def save(self):
        '''Add object to database.'''
        try:
            self.id = getattr(db, self.tablename)[-1]['id']+1
        except IndexError:
            self.id = 1
        current = self.current()
        getattr(db, self.tablename).append(current)
        return self.view()


    def view(self):
        '''View object as a dictionary.'''

        return self.current


class Product(Base):
    '''Product model.'''

    def __init__(self, name, price):
        '''Initialize a product.'''

        self.id = 0
        self.name = name
        self.price = price
        self.tablename = 'products'

    def current(self):
        '''Current product'''
        current = {
            "name": self.name,
            "price": self.price,
            "id": self.id
        }
        return current

    def view(self):
        '''View product's information.'''

        return {
            "name": self.name,
            "price": self.price,
            "id": self.id
        }

class Sale(Base):
    '''Sales model.'''

    def __init__(self, name, price):
        '''Initialize a sale.'''

        self.id = 0
        self.name = name
        self.price = price
        self.tablename = 'sales'

    def current(self):
        '''Current sale'''
        current = {
            "name": self.name,
            "price": self.price,
            "id": self.id
        }
        return current

    def view(self):
        '''View a user's information.'''

        return {
            "name": self.name,
            "price": self.price,
            "id": self.id
        }

class User(Base):
    '''User model.'''

    def __init__(self, username, password, email, is_admin, is_attendant, id=None):
        '''Initialize a user.'''

        self.id = 0
        self.username = username
        self.email = email
        self.password = self.make_hash(password)
        if str(is_admin) == 'True':
            self.is_admin = True
        else:
            self.is_admin = False
        if str(is_attendant) == 'True':
            self.is_attendant = True
        else:
            self.is_attendant = False
        self.tablename = 'users'

    def current(self):
        '''Current user'''
        current = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'is_attendant': self.is_attendant,
            'is_admin': self.is_admin,
            'id': self.id
        }
        return current

    def view(self):
        '''View a user's information.'''

        return {
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_attendant': self.is_attendant,
            'id': self.id
        }

    def make_hash(self, password):
        '''Generate hash of password.'''

        return sha256(password.encode('utf-8')).hexdigest()

    def generate_token(self):
        '''Create a token for a user.'''

        key = getenv('APP_SECRET_KEY')
        payload = {
            'user_id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'is_attendant': self.is_attendant
        }
        return jwt.encode(payload=payload, key=str(key), algorithm='HS256').decode('utf-8')


    @staticmethod
    def decode_token(token):
        '''View information inside a token.'''

        return jwt.decode(token, key=str(getenv('APP_SECRET_KEY')))

    def check_password(self, password):
        '''Validate a user's password.'''
