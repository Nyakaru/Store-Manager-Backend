"""Database handling resource."""

from os import getenv

from app import conn


conn.set_session(autocommit=True)
cur = conn.cursor()


class BaseModel():
    '''Base class for models.'''

    def save(self):
        '''Save item.'''
        conn.commit()

    def close(self):
        '''close'''
        cur.close()
        conn.close()

    def get(self):
        '''Get item fom db.'''
        pass

    def delete(self):
        '''Delete Item from db.'''
        pass

    def update(self):
        '''Update Item details.'''
        pass
