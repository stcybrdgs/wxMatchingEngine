# import library components  ---------------------------------------------------
import os, shutil, sys
import pathlib
from pathlib import Path
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

# import py files  -------------------------------------------------------------
import generate_brand_patterns
import get_brands_db_iesa
import get_brands_db_wx
import get_data_org_iesa
import get_data_cln_iesa
import get_data_cln_org_iesa
import tbd

# global variables  ------------------------------------------------------------
menu_options = []
menu_functions = []
menu_choices = []
menu_options = [
    'Get brands (IESA.ProductsClean)',
    'Get brands (WrWx.Brands)',
    'Get original data (IESA.ProductsOriginal)',
    'Get clean data (IESA.ProductsClean)',
    'Get clean + original data (IESA.ProductsOriginal JOIN IESA.ProductsClean)',
    'Generate brands patterns for NERS',
    'Extract brands with NERS (ad hoc)',
    'Extract brands with NERS (IESA model)'
    ]
menu_functions = [
    get_brands_db_iesa,
    get_brands_db_wx,
    get_data_org_iesa,
    get_data_cln_iesa,
    get_data_cln_org_iesa,
    generate_brand_patterns,
    tbd,
    tbd
]
num_menu_items = 0

# helper functinos  ------------------------------------------------------------
def show_main_menu():
    global num_menu_items
    global menu_choices
    num_menu_items = 0
    # print user menu
    print('\n-----------------------------------------')
    print('           Main Menu - Brand Tasks')
    print('-----------------------------------------')
    spacer ='   '
    print('{}{}{}'.format('m', spacer, 'Show Main Menu'))
    print('{}{}{}'.format('e', spacer, 'Exit Program'))
    menu_choices.append('e')
    menu_choices.append('m')
    for opt in menu_options:
        num_menu_items += 1
        if num_menu_items < 10: spacer = '   '
        else: spacer = '  '
        print('{}{}{}'.format(num_menu_items, spacer, opt))
        menu_choices.append(str(num_menu_items))
    print('\n')

# main program  ----------------------------------------------------------------
def main():
    global menu_choices
    global menu_functions
    global num_menu_items

    # print menu options to console  -------------------------------------------
    show_main_menu()

    is_program_running = True
    while is_program_running:
        # get & validate user input
        print('Select a task (or \'m\' for menu, \'e\' to exit): ')
        menu_choice = input()
        while menu_choice not in menu_choices:
            print('Invalid choice! Select a task: ')
            menu_choice = input()

        # execute user-selected task
        if menu_choice == 'e': is_program_running = False
        elif menu_choice == 'm': show_main_menu()
        else:
            print('\n-----------------------------------------')
            print('You selected: {}'.format(menu_options[int(menu_choice)-1]))
            index = int(menu_choice)-1
            print('\nRunning module: ')
            print(menu_functions[index])
            menu_functions[index].main()

if __name__ == '__main__' : main()
