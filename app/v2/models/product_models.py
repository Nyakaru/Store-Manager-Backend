'''Products model.'''

from os import getenv

from app.v2.connect_db import connect_to_db


conn = connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur = conn.cursor()


class Product(object):
    '''product model.'''

    def __init__(self, name, price,quantity):
        '''Initialize a product.'''
        self.id = None
        self.name = name
        self.price = price
        self.quantity = quantity
        

    def save(self):
        '''save item to db'''
        conn.commit()

    def add_product(self):
        '''Add product details to db table.'''
        cur.execute(
            """
            INSERT INTO products(name, price, quantity)
            VALUES(%s,%s,%s)
            """,
            (self.name, self.price, self.quantity)
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
        

    @classmethod
    def update(self, id, new_data):
        '''Update product details given new information.'''
        for key, val in new_data.items():
            cur.execute("""
            UPDATE products SET {}='{}' WHERE id={}
            """.format(key, val, id))


    @staticmethod
    def get(**kwargs):
        '''Get product by key'''
        for key, val in kwargs.items():
            query = "SELECT * FROM products WHERE {}='{}'".format(key, val)
            cur.execute(query)
            product = cur.fetchone()
            return product

    @classmethod
    def get_cost(cls, product_id, quantity=1):
        '''Calculate the cost of a product given price and quantity'''
        price = cls.get(id=product_id)[2]
        return price*quantity

    @staticmethod
    def view(product):
        '''View a product information.'''
        id = product[0]
        return {
            'id': id,
            'name': product[1],
            'price': product[2],
            'quantity':product[3]
        }
