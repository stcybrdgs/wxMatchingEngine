#!/usr/bin/python
import sqlite3, sys, os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'testDB.sqlite3')

def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

con = db_connect()
cur = con.cursor()
print('Opened database succesfully.')

create_table_sql = """
    CREATE TABLE tester(
    ID INT PRIMARY KEY NOT NULL,
    NAME TEXT NOT NULL,
    AGE INT NOT NULL
    )
    """
cur.execute(create_table_sql)

insert_records_sql = "INSERT INTO tester (ID, NAME, AGE) VALUES (?, ?, ?)"
names = ['Jo','Ann','Bo','Dee','Ra']
ages = [12,13,14,15,16]
i = 0
for name in names:
    cur.execute(insert_records_sql, (i, names[i], ages[i]))
    i += 1

con.commit()
con.close()

print('Done.')
