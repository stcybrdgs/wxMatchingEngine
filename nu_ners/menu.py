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

# helper functinos  ------------------------------------------------------------
def show_main_menu():
    global num_menu_items
    global menu_choices
    menu_choices.clear()
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

def show_submenu(menu_title, file_choices):
    global menu_choices
    menu_choices.clear()
    # print user menu
    print('\n-----------------------------------------')
    print('           ' + menu_title)
    print('-----------------------------------------')
    spacer ='  '
    print('{}{}{}'.format('m', spacer, 'Show Main Menu'))
    menu_choices.append('m')
    i = 0
    for ic in file_choices:
        i += 1
        print('{}  {}'.format(i, ic))
        menu_choices.append(str(i))

def extract_brands_ners_adhoc_menu():
    #print('This is the Menu Driver for \'NERS - extract Brands (ad hoc)\'')
    # check for jsonl file
    #    if none, alert;
    #    else confirm user wants to use existing file
    # check for data file; if none, alert
    # if jsonl && data present data files and ask user to pick one
    # after user picks one, run extract_brands_ners_adhoc()

    # get the user's choice of which jsonl file to use -------------------------
    # print menu options to console
    # declare menu and file arrays
    #menu_choices = []
    #data_file_choices = []
    jsonl_file_exists = False
    jsonl_files = []
    jsonl_choice = ''

    # get path of current folder
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # get names of .xlsx files that are in the folder that are also input files
    for r, d, f in os.walk(folder_path):  # rem r=root, d=dir, f=file
        for file in f:
            #print(file)
            if 'ners' in file and 'patterns' in file and 'jsonl' in file:
                # rem for full path use <files.append(os.path.join(r, file))>
                jsonl_file_exists = True
                #jsonl_files.append(file)
                jsonl_files.append(file)
                #break

    if jsonl_file_exists:
        show_submenu('NERS - Select patterns', jsonl_files)
        #print('SUBMENU TEST: the files are:')
        #for file in jsonl_files:
            #print(file)
    else:
        # if there is no JSONL file, redirect the user to the main menu
        # so that they can make one
        print('You need a JSONL patterns file to run this task. To make one, press \'m\' to return to the main menu.')
        user_input = input()
        while user_input != 'm':
            print('Invalid input. Press \'m\' to return to the main menu.')
            user_input = input()
        main()
        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this function; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()

    # get user input
    print('\nSelect an input file (or \'m\' for Main Menu)')
    jsonl_choice = input()

    # validate user input
    while jsonl_choice not in menu_choices:
        print('Invalid choice! Select an input file (or \'m\' for Main Menu)')
        jsonl_choice = input()

    if jsonl_choice == 'm':
        main()
        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this program; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()
    else:
        jsonl_choice = jsonl_files[int(jsonl_choice)-1]
        print('\nYou chose: {}'.format(jsonl_choice))
        #print(jsonl_files)

    # get the user's choice of which tender file to use ------------------------
    # print menu options to console
    # declare menu and file arrays
    #menu_choices = []
    #data_file_choices = []
    tender_file_exists = False
    tender_files = []
    tender_choice = ''

    # get path of current folder
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # get names of .xlsx files that are in the folder that are also input files
    for r, d, f in os.walk(folder_path):  # rem r=root, d=dir, f=file
        for file in f:
            #print(file)
            if 'db_data' in file:
                # rem for full path use <files.append(os.path.join(r, file))>
                tender_file_exists = True
                #jsonl_files.append(file)
                tender_files.append(file)
                #break

    if tender_file_exists:
        show_submenu('NERS - Select tender', tender_files)
        #print('SUBMENU TEST: the files are:')
        #for file in jsonl_files:
            #print(file)
    else:
        # if there is no tender file, redirect the user to the main menu
        # so that they can make one
        print('You need a \'db_data\' file to run this task. To make one, press \'m\' to return to the main menu, then choose \'Get Data\'.')
        #user_input.clear()
        user_input = input()
        while user_input != 'm':
            print('Invalid input. Press \'m\' to return to the main menu.')
            user_input = input()
        main()
        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this function; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()

    # get user input
    print('\nSelect an input file (or \'m\' for Main Menu)')
    tender_choice = input()

    # validate user input
    while tender_choice not in menu_choices:
        print('Invalid choice! Select an input file (or \'m\' for Main Menu)')
        tender_choice = input()

    if tender_choice == 'm':
        main()
        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this program; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()
    else:
        tender_choice = tender_files[int(tender_choice)-1]
        print('\nYou chose: {}'.format(tender_choice))
        #print(tender_files)

    print('\nDo you want to extract brands using the following files (y/n)?')
    print(jsonl_choice)
    print(tender_choice)
    yn_input = input()
    while yn_input not in ('y', 'n'):
        print('\nInvalid input.')
        print('Do you want to extract brands using the following files (y/n)?')
        print('   {}'.format(jsonl_choice))
        print('   {}'.format(tender_choice))
        yn_input = input()

    if yn_input == 'y':
        # call the extract function
        #extract_brands_ners_adhoc(jsonl_choice, tender_choice)
        # update user selections to reflect full path
        jsonl_choice = folder_path + '\\' + jsonl_choice
        tender_choice = folder_path + '\\' + tender_choice
        print('\nExtracting Brands...')
        extract_brands_ners_adhoc.main(jsonl_choice, tender_choice)
    else:
        main()
        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this function; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()

# global variables  ------------------------------------------------------------
menu_options = []
menu_functions = []
menu_choices = []
menu_options = [
    'Session - Start logging',
    'Session - Archive session',
    'Session - Clean session',
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
    'NERS - extract MPNs (IESA model)',
    'NERS - manage Displacy Visualizer'
    ]
menu_functions = [
    tbd,
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
    extract_brands_ners_adhoc_menu,
    tbd,
    tbd,
    tbd,
    tbd
]
num_menu_items = 0

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
        # handle 'm' and 'e'
        if menu_choice == 'e': is_program_running = False
        elif menu_choice == 'm': show_main_menu()

        # test menu driver for NERS - extract Brands (ad hoc)
        else:
            index = int(menu_choice)-1
            if menu_options[index] == 'NERS - extract Brands (ad hoc)':
                menu_functions[index]()
            else:
                print('\n-----------------------------------------')
                print('You selected: {}'.format(menu_options[int(menu_choice)-1]))
                index = int(menu_choice)-1
                print('\nRunning module: ')
                print(menu_functions[index])
                menu_functions[index].main()

if __name__ == '__main__' : main()
