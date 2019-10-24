# import library components  ---------------------------------------------------
# import shutil
import os, sys
import pyodbc
import pathlib
from pathlib import Path
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

# import py files  -------------------------------------------------------------
import menu

# global variables  ------------------------------------------------------------
menu_nums = []
menu_choices = []

# helper functions  ------------------------------------------------------------
def get_menu_choices():
    # rem use SQL query to get the categories
    choices = ['Show Main Menu', 'MechPT', 'Electrical', 'FluidPower', 'PPE', 'Tools']
    return choices

def show_menu():
    global menu_nums
    global menu_choices

    # print user menu
    print('\n-----------------------------------------')
    print('           Get Original Data - Categories Menu')
    print('-----------------------------------------')
    spacer ='  '
    menu_choices = get_menu_choices()

    i = 0
    num = ''
    for mc in menu_choices:
        if i == 0:
            num = 'm'
        else:
            num = str(i)
        print('{}{}{}'.format(num, spacer, mc))
        menu_nums.append(num)
        i += 1

def get_user_choice():
    global menu_choices
    # get user choice
    print('\nSelect a category (or \'m\' for Main Menu)')
    user_choice = input()

    # validate user input
    while user_choice not in menu_nums:
        print('Invalid choice! Select a category (or \'m\' for Main Menu)')
        user_choice = input()

    if user_choice == 'm':
        menu.main()

        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this program; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()
    else:
        index = int(user_choice)
        return menu_choices[int(user_choice)]

# main  ------------------------------------------------------------------------
def main():
    print('You called \'get_data_cln_iesa.py\'')  # temp message
    show_menu()  # show the menu of category choices
    category = get_user_choice()  # get user choice of category

    # connect to db and query for data per user-selected category
    print('You selected the category \'' + category + '\'')
    print('Connecting to the database...')

    # connection info
    server = 'sql.wrangle.works'
    database = 'IESA'
    username = 'stacy'
    password = '8d39c!76b8d1'
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    # query info
    data_query = [
        'SELECT '
        'ID, ProductCategory, Brand, ',
    	'ManufacturerID as MPN, UNSPSC, LongText, SupplementaryDetails ',
        'FROM ProductsClean ',
        'WHERE ProductCategory = \'' + category + '\' ORDER BY ID ASC'
        ]

    sql = ''
    for str in data_query:
        sql = sql + str + ' '

    cursor = connection.cursor().execute(sql)

    # create dictionary of results from query
    columns = [column[0] for column in cursor.description]
    results = []
    record_count = 0
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
        record_count += 1
        print('record {}'.format(record_count))

    # parse the list of data dictionaries that was created in the previous step
    # so that you have a pd array for each db column that was returned by sql query
    # ... but first, identify your pd arrays
    id = []
    productCategory = []
    brand = []
    mpn = []
    unspsc = []
    longText = []
    supplementaryDetails = []

    # put the pd arrays into a master array so that you can iterate through them
    pd_arrays = [id, productCategory, brand, mpn, unspsc, longText, supplementaryDetails]

    # now, iterate through the master array, and parse your list of dicts
    # into the individual pd arrays
    print('\nWriting results to dataframe...')
    for d in results:
        index = 0
        for k,v in d.items():
            pd_arrays[index].append(v)
            index +=1

    # print query results to excel file  ---------------------------------------
    df = pd.DataFrame({
        'ID':id,
        'ProductCategory':productCategory,
        'Brand':brand,
        'MPN':mpn,
        'UNSPSC':unspsc,
        'LongText':longText,
        'SupplementaryDetails':supplementaryDetails
    })
    data_file_path = folder_path = os.path.dirname(os.path.abspath(__file__))
    data_file_name = 'db_data_cln_iesa_' + category + '.xlsx'
    outfile = data_file_path + '\\' + data_file_name
    writer = pd.ExcelWriter(outfile)
    df.to_excel(writer,'Sheet1', index=False)
    writer.save()

    # end program
    print('\n')
    print('{} records written'.format(record_count))
    print(data_file_name)
    print(outfile)
    print('Done.')

if __name__ == '__main__' : main()
