from os import getenv

from app.v2.connect_db import connect_to_db
from app.v2.models.product_models import Product


conn=connect_to_db(getenv('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur=conn.cursor()


class Sale:
    '''Sale model.'''

    def __init__(self, user_id, product_dict):
        '''
        Create a sale.
        '''
        self.user_id = user_id
        self.product_dict = product_dict

    def save(self):
        '''save item to db'''
        conn.commit()

    def add_sale(self):
        '''Add sale details to table.'''
        cur.execute(
            """
            INSERT INTO sales(user_id)
            VALUES({}) RETURNING id;
            """.format(self.user_id)
        )
        self.id = cur.fetchone()[0]
        self.save()
        self.make_sale_items()
        return self.id

    def make_sale_items(self):
        '''Add a sale item.'''
        print(self.product_dict)
        for key, val in self.product_dict.items():
            cur.execute(
                """
                INSERT INTO sale_items(sale_id, product_id, quantity)
                VALUES({}, {}, {}) RETURNING id
                """.format(self.id, key, val)
            )
            self.save()

    @staticmethod
    def get(**kwargs):
        '''Get sale by key'''
        for key, val in kwargs.items():
            query="SELECT * FROM sales WHERE {}='{}'".format(key,val)
            cur.execute(query)
            sale = cur.fetchone()
            return sale
    
    @staticmethod
    def get_all_by_user_id(user_id):
        '''Get sales belonging to a certain user'''
        query = "SELECT * FROM sales WHERE user_id='{}'".format(user_id)
        cur.execute(query)
        sales = cur.fetchall()
        return sales

    @staticmethod
    def get_products(sale_id):
        '''Get all products of a sale.'''
        cur.execute(
            """
            SELECT * FROM sale_items WHERE sale_id={}
            """.format(sale_id))
        sale_items = cur.fetchall()
        return [{
            "product_id": item[1],
            "product_name":Product.get(id=item[1])[1],
            "sale_item_id":item[0],
            "quantity":item[3]
        } for item in sale_items]

    @staticmethod
    def view(sale):
        '''View sale details.'''
        sale_id, user_id = sale[0], sale[1]
        products = Sale.get_products(sale_id)
        total = Sale.total(sale_id)
        return {
            'sale_id': sale_id,
            'user_id': user_id,
            'products': products,
            'total': total
        }

    @staticmethod
    def get_all():
        '''Get all sales.'''
        query = "SELECT * FROM sales"
        cur.execute(query)
        sales = cur.fetchall()
        return sales

    @classmethod
    def total(cls, sale_id):
        '''Calculate total cost of a sale.'''
        sale_items = cls.get_products(sale_id=sale_id)
        cost = 0
        for sale_item in sale_items:
            cost += Product.get_cost(product_id=sale_item["product_id"], quantity=sale_item["quantity"])
        return cost
