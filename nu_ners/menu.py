#!/usr/bin/env python
"""
Wed, Oct 23, 2019
Stacy Bridges

"""
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
import add_wx_cols
import extract_brands_ners_adhoc

import tbd
# global variables  ------------------------------------------------------------
menu_options = []
menu_functions = []
menu_choices = []
menu_options = [
    'Session - Start logging',
    'Session - Archive session',
    'Get Brands (IESA.ProductsClean)',
    'Get Brands (WrWx.Brands)',
    'Get Data - Original (IESA.ProductsOriginal)',
    'Get Data - Clean (IESA.ProductsClean)',
    'Get Data - Clean + Original (IESA.ProductsOriginal JOIN IESA.ProductsClean)',
    'Add WrWx columns to data file',
    'NERS - generate patterns for Brands (JSONL)',
    'NERS - generate patterns for MPNs (JSONL)',
    'NERS - extract Brands (ad hoc)',
    'NERS - extract Brands (IESA model)',
    'NERS - extract MPNs (ad hoc)',
    'NERS - extract MPNs (IESA model)'
    ]
menu_functions = [
    tbd,
    tbd,
    get_brands_db_iesa,
    get_brands_db_wx,
    get_data_org_iesa,
    get_data_cln_iesa,
    get_data_cln_org_iesa,
    add_wx_cols,
    generate_brand_patterns,
    tbd,
    extract_brands_ners_adhoc,
    tbd,
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
        print('\nSelect a task (or \'m\' for menu, \'e\' to exit): ')
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
