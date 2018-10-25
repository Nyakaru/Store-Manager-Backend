'''Productss model.'''

from os import getenv

from api.v2.connect_to_db import connect_to_db


conn = connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur = conn.cursor()


class Product(object):
    '''product model.'''

    def __init__(self, name, price):
        '''Initialize a product.'''
        self.id = None
        self.name = name
        self.price = price

    def save(self):
        '''save item to db'''
        conn.commit()

    def add_product(self):
        '''Add product details to db table.'''
        cur.execute(
            """
            INSERT INTO products(name, price)
            VALUES(%s,%s)
            """,
            (self.name, self.price)
        )
        self.save()

    @staticmethod
    def get_all():
        '''Get all products.'''
        query = "SELECT * FROM products"
        cur.execute(query)
        products = cur.fetchall()
        return products

    @classmethod
    def delete(cls, id):
        '''Delete a product from db.'''
        query = "DELETE FROM products WHERE id={}".format(id)
        cur.execute(query)
        cls.save(cls)

    @classmethod
    def update(cls, id, new_data):
        '''Update product details given new information.'''
        for key, val in new_data.items():
            cur.execute("""
            UPDATE products SET {}='{}' WHERE id={}
            """.format(key, val, id))
            cls.save(cls)

    @staticmethod
    def get(**kwargs):
        '''Get product by key'''
        for key, val in kwargs.items():
            querry = "SELECT * FROM products WHERE {}='{}'".format(key, val)
            cur.execute(querry)
            product = cur.fetchone()
            return product

    @staticmethod
    def view(product):
        '''View a product information.'''
        id = product[0]
        return {
            'id': id,
            'name': product[1],
            'price': product[2]
        }
