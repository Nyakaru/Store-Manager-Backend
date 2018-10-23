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

class Sale(Base):
    '''Sales model.'''

    def __init__(self, name, price):
        '''Initialize a sale.'''

        self.id = 0
        self.name = name
        self.price = price
        self.tablename = 'sales'

    def current(self):
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

    def __init__(self, username, password, email, isAdmin, isAttendant, id=None):
        '''Initialize a user.'''

        self.id = 0
        self.username = username
        self.email = email
        self.password = self.make_hash(password)
        if str(isAdmin) == 'True':
            self.isAdmin = True
        else:
            self.isAdmin = False
        if str(isAttendant) == 'True':
            self.isAttendant = True
        else:
            self.isAttendant = False
        self.tablename = 'users'


    def current(self):
        current = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'isAttendant': self.isAttendant,
            'isAdmin': self.isAdmin,
            'id': self.id
        }
        return current

    def view(self):
        '''View a user's information.'''

        return {
            'username': self.username,
            'email': self.email,
            'isAdmin': self.isAdmin,
            'isAttendant': self.isAttendant,
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
            'isAdmin': self.isAdmin,
            'isAttendant': self.isAttendant
        }
        return jwt.encode(payload=payload, key=str(key), algorithm='HS256').decode('utf-8')


    @staticmethod
    def decode_token(token):
        '''View information inside a token.'''

        return jwt.decode(token, key=str(getenv('APP_SECRET_KEY')))

    def check_password(self, password):
        '''Validate a user's password.'''
