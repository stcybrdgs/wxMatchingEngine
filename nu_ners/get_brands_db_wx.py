# get_brands_db_wx.py

# import library components  ---------------------------------------------------
# import shutil
import os
import pyodbc
import pathlib
from pathlib import Path
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

def main():
    # get path of current folder
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # identify i/o  ----------------------------------------------------------------
    outfile_name = 'db_brands_wx.xlsx'
    outfile_path = folder_path + '\\' + outfile_name

    # connection & query info  -----------------------------------------------------
    print('\nConnecting to database...')
    server = 'sql.wrangle.works'
    database = 'Wrangleworks'
    username = 'stacy'
    password = '8d39c!76b8d1'
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    # cursor info
    cursor = connection.cursor()

    # query info
    brand_query = ['''
        SELECT DISTINCT ID
        FROM Brands
        ORDER BY ID ASC
        ''']
    brands = []

    # fetch brands from database  --------------------------------------------------
    # fetch brands, append them to pandas array, and print them to console
    print('\nQuerying the database...')
    cursor.execute(brand_query[0]) # reset the cursor
    row = cursor.fetchone()
    row_count = 0
    while row:
        for i in row:
            print('{}'.format(i), end='')
            brands.append(i)
            row_count += 1
        row = cursor.fetchone()
        print('')

    # print query results to excel file  -------------------------------------------
    df = pd.DataFrame({'BRAND':brands})
    writer = pd.ExcelWriter(outfile_path)
    df.to_excel(writer,'Sheet1', index=False)
    writer.save()

    # end program  -----------------------------------------------------------------
    print('\n{} Brands written'.format(row_count))
    print(outfile_path)
    print('Done.')

if __name__ == '__main__' : main()
