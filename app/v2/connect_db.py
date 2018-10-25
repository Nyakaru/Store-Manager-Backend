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
    
    default_conn = connect(
        database=os.getenv('D_DB'),
        user='postgres',
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'))
    default_conn.set_session(autocommit=True)
    cur = default_conn.cursor()
    dev_db = os.getenv('DEV_DB')
    test_db = os.getenv('TESTING_DB')

    if check_if_db_exists(dev_db) is False:
        query = "CREATE DATABASE {}".format(dev_db)
        cur.execute(query)
    
    if check_if_db_exists(test_db) is False:
        query = "CREATE DATABASE {}".format(test_db)
        cur.execute(query)  
    

#     dev_db = "CREATE DATABASE IF NOT EXISTS " + os.getenv('DEV_DB')
#     test_db = "CREATE DATABASE IF NOT EXISTS " + os.getenv('DEV_DB')

def connect_to_db(db=None):
    '''create a connection to the right db.'''

    if db == 'testing':
        db_name = os.getenv('TESTING_DB')
    else:
        db_name = os.getenv('DEV_DB')
        
    try:

        return connect(
            database=db_name,
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'))
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
            price INTEGER NOT NULL
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
        """DROP TABLE IF EXISTS users, products, roles, user_roles CASCADE
        """)

    # create the tables
    user_table(cur)
    roles(cur)
    user_roles(cur)
    products_table(cur)
    make_roles(cur, conn)

    cur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_databases()
    create()
