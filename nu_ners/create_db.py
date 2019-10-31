from db_utils import db_connect

con = db_connect() # connect to the database
cur = con.cursor() # instantiate a cursor obj

customers_sql = """
    CREATE TABLE customers (
    id integer PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL)"""

cur.execute(customers_sql)

products_sql = """
    CREATE TABLE products (
    id integer PRIMARY KEY,
    name text NOT NULL,
    price real NOT NULL)"""

cur.execute(products_sql)

con.close()

print('Done.')
