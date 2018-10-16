'''Models and their methods.'''

class DB():
    '''In memory database.'''

    def __init__(self):
        '''Create an empty database.'''

        self.products = {}
        self.sales = {}

    def drop(self):
        '''Drop entire database.'''

        self.__init__()


db = DB()


class Base:
    '''Base class to be inherited by other models.'''

    def save(self):
        '''Add object to database.'''

        if self.id is None:
            setattr(self, 'id', len(getattr(db, self.tablename)) + 1)
        getattr(db, self.tablename).update({self.id: self})
        return self.view()

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

    @classmethod
    def get_many_by_key(cls, **kwargs):
        '''Get an object by a key that is not id.'''

        kwarg = list(kwargs.keys())[0]
        db_store = getattr(db, cls.tablename)
        objs = []
        for key in db_store:
            obj = db_store[key]
            if obj.view()[kwarg] == kwargs[kwarg]:
                objs.append(obj)
        return objs

class Product(Base):
    '''Product model.'''

    tablename = 'products'

    def __init__(self, name, price):
        '''Initialize a product.'''

        self.id = None
        self.name = name
        self.price = price



class Sales(Base):
    '''Sales model.'''

    tablename = 'sales'

    def __init__(self, sales_dict):
        '''
        Create a sale.

        Pass in sales_dict as {sale_id: quantity}
        '''
        self.id = None
        self.sales = [
            {'quantity': sales_dict[sale_id],
             'sale': sale.get(id=int(sale_id)).view()}
            for sale_id in sales_dict.keys()]
        self.total = self.get_total()

    def get_total(self):
        '''Get total cost of a sale.'''
        return sum([i['quantity'] * i['sale']['price'] for i in self.sales])

