'''postgreql db connection'''

import os
from psycopg2 import connect

def check_if_db_exists(db_name):
    '''check is a specified db exists.'''  
    try:  
        conn = connect(
                database=db_name,
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'))
        return True
    except:        
        return False

def create_databases():
    
    default_conn = connect(os.getenv('DEV_DB'))
    default_conn.set_session(autocommit=True)

    cur = default_conn.cursor()
    dev_db = os.getenv('DEV_DB')
    test_db = os.getenv('TESTING_DB')
    

#     dev_db = "CREATE DATABASE IF NOT EXISTS " + os.getenv('DEV_DB')
#     test_db = "CREATE DATABASE IF NOT EXISTS " + os.getenv('DEV_DB')

def connect_to_db(db=None):
    '''create a connection to the right db.'''
        
    try:

        return connect(os.getenv('DEV_DB'))
    except:
        return "Unable to connect"

def user_table(cur):
    '''Define users table'''
    cur.execute(
        """
        CREATE TABLE users(
            id serial PRIMARY KEY,
            username VARCHAR NOT NULL UNIQUE,
            email VARCHAR NOT NULL UNIQUE ,
            password VARCHAR NOT NULL,
            roles BOOLEAN NOT NULL DEFAULT FALSE
        );
        """
    )

def roles(cur):
    '''Create user roles.'''

    cur.execute(
        """
        CREATE TABLE roles(
            id serial PRIMARY KEY,
            name VARCHAR NOT NULL);
        """
    )

# many to many user-role relationship
def user_roles(cur):
    '''Create user roles.'''
    cur.execute(
        """
        CREATE TABLE user_roles(
            user_id INTEGER,
            role_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
            constraint id PRIMARY KEY (user_id, role_id)
        );
        """
    )

def products_table(cur):
    '''Define products table.'''
    cur.execute(
        """
        CREATE TABLE products(
            id serial PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        );
        """
    )

def sales_table(cur):
    '''Define sales table.'''
    cur.execute(
        """
        CREATE TABLE sales(
            id serial PRIMARY KEY,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

def sale_item(cur):
    '''Create sale item.'''
    cur.execute(
        """
        CREATE TABLE sale_items(
            id serial PRIMARY KEY,
            product_id INTEGER NOT NULL,
            sale_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE
        );
        """
    )


def make_roles(cur, conn):
    '''Add admin, user and superuser roles to the roles table.'''
    cur.execute("INSERT INTO roles(name)  VALUES('user')")
    cur.execute("INSERT INTO roles(name) VALUES('admin')")
    cur.execute("INSERT INTO roles(name) VALUES('superuser')")
    conn.commit()

def create(db=None):
    '''Create all required tables.'''
    conn = connect_to_db(db=db)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute(
        """DROP TABLE IF EXISTS users, products, sales, roles, user_roles, sale_items CASCADE
        """)

    # create the tables
    user_table(cur)
    roles(cur)
    user_roles(cur)
    products_table(cur)
    sales_table(cur)
    sale_item(cur)
    make_roles(cur, conn)

    cur.close()
    conn.commit()
    


if __name__ == '__main__':
    create_databases()
    create()



