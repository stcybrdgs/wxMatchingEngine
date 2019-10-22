# import library components  ---------------------------------------------------
import os, shutil
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
import tbd

# helper functinos  ------------------------------------------------------------
def show_main_menu():
    pass

def exit_program():
    pass

# main program  ----------------------------------------------------------------
def main():
    # print menu options to console  -------------------------------------------
    menu_options = [
        'Get Brands (IESA.ProductsClean)',
        'Get Brands (WrWx.Brands)',
        'Get original data (IESA.ProductsOriginal)',
        'Get clean data (IESA.ProductsClean)',
        'Get clean + original data (IESA.ProductsOriginal JOIN IESA.ProductsClean)',
        'Generate Brands patterns for NERS',
        'Extract Brands with NERS (ad hoc)',
        'Extract Brands with NERS (IESA model)',
        'Show the main menu',
        'Exit the program'
        ]
    menu_functions = [
        get_brands_db_iesa,
        get_brands_db_wx,
        tbd,
        tbd,
        tbd,
        generate_brand_patterns,
        tbd,
        tbd,
        show_main_menu,
        exit_program
    ]
    menu_choices = []

    # print user menu
    print('\n-----------------------------------------')
    print('           Main Menu - Brand Tasks')
    print('-----------------------------------------')
    i = 0
    spacer =''
    for opt in menu_options:
        i += 1
        if i < 10: spacer = '   '
        else: spacer = '  '
        print('{}{}{}'.format(i, spacer, opt))
        menu_choices.append(str(i))
    print('\n')

    # get user input
    print('Select a task (1-{}): '.format(i))
    menu_choice = input()

    # validate user input
    while menu_choice not in menu_choices:
        print('Invalid choice! Select an input (1-{}): '.format(i))
        menu_choice = input()

    # execute user-selected task
    index = int(menu_choice)-1
    print('\nRunning module: ')
    print(menu_functions[index])
    menu_functions[index].main()

if __name__ == '__main__' : main()
