#!/usr/bin/env python
# coding: utf8
"""
Sun 9/8/2019
Stacy

user runs add_wxcols.py from command line
>> python add_wxcols.py
- make a copy of the project file and save with a '_wx_v1' suffix
- add the wx columns
- rename add_wxcols.py as py_add_wxcols.py and move to the ners folder

intro to xlsxwriter library at:
https://pbpython.com/improve-pandas-excel-output.html
and
https://xlsxwriter.readthedocs.io/

"""
# IMPORTS  ---------------------------------------------------------------------
import os, shutil, sys
import pathlib
from pathlib import Path
import shutil
from hashids import Hashids
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell  # excel formatting

# import py files  -------------------------------------------------------------
import menu

def main():
    # print menu options to console  -----------------------------------------------
    # declare menu and file arrays
    menu_choices = []
    file_choices = []
    console_message = ''

    # get path of current folder
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # get names of .xlsx files that are in the folder that are also input files
    for r, d, f in os.walk(folder_path):  # rem r=root, d=dir, f=file
        for file in f:
            if '.xlsx' in file and 'data' in file and '_wx_v1' not in file:
                # rem for full path use <files.append(os.path.join(r, file))>
                file_choices.append(file)

    # print user menu
    print('\n-----------------------------------------')
    print('           Data Files')
    print('-----------------------------------------')
    spacer ='  '
    print('{}{}{}'.format('m', spacer, 'Show Main Menu'))
    menu_choices.append('m')
    i = 0
    for ic in file_choices:
        i += 1
        print('{}  {}'.format(i, ic))
        menu_choices.append(str(i))

    # get user input
    if len(file_choices) == 0:
        console_message = '\nNo data files available. Select \'m\' for Main Menu'
    else:
        console_message = '\nSelect a data file (or \'m\' for Main Menu)'
    print(console_message)
    user_choice = input()

    # validate user input
    while user_choice not in menu_choices:
        print('Invalid choice! {}'.format(console_message))
        user_choice = input()

    if user_choice == 'm':
        menu.main()

        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this program; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()

    # see if user-selected file has already been made into a wx_v1 file
    user_selected_file = file_choices[int(user_choice)-1]
    wx_files = []
    wx_file_exists = False
    # find wx_v1 filenames and put them in array
    for r, d, f in os.walk(folder_path):  # rem r=root, d=dir, f=file
        for file in f:
            if 'xlsx' in file and 'wx_v1' in file:
                wx_files.append(file)

    for f in wx_files:
        if user_selected_file[0:len(user_selected_file)-5] in f:
            wx_file_exists = True

    # if the wx_v1 file already exists, see if user wants to overwrite it
    want_to_add_cols = True
    if wx_file_exists:
        print('A \'wx_v1\' file already exists for that data. Overwrite (y/n)?')
        yn_choice = input()
        while yn_choice not in ['y', 'n', 'Y', 'N']:
            print('Invalid choice! Overwrite (y/n)?')
            yn_choice = input()
        if yn_choice == 'n':
            want_to_add_cols = False

    # if the user wants to overwrite the existing wx_1 file, or
    # if there is not yet a wx_1 file for the user-selected data file, then
    # create the new wx_1 file
    if want_to_add_cols:
        print('\nAdding wx columns to \'' + user_selected_file + '\' ...')

        # define paths/names for files and directories
        mkpath = os.path.abspath(__file__)  # = (os.path.abspath('.'))
        projectDir = os.path.dirname(mkpath)
        #templateDir = os.path.dirname(projectDir) + r'\NERS_Template'  # relative path
        #nersDir = projectDir + r'\ners'
        #projectFile = ''
        #projectFilename = ''
        projectSheetName = ''
        metaDir = projectDir + r'\input'  # relative path
        metaFilename = r'\in_wxmeta.xlsx'
        metaFile = metaDir + metaFilename
        wxFile = ''
        wxFilename = ''
        wxSheetName = 'WrWx Fields'
        numberOfRows = 0
        hashids = Hashids(alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=5)

        # get the name of the project file
        wxFilename = user_selected_file[0:len(user_selected_file)-5] + '_wx_v1.xlsx'
        wxFile = projectDir + '\\' + wxFilename
        '''
        count_xlsx = 0
        for item in os.listdir(projectDir):
            name = os.path.splitext(item)[0]
            ext = os.path.splitext(item)[1]
            if count_xlsx > 1:
                # throw an error if there is more than one project file
                print('Error: There can be only one .xlsx file at the base of {}'.format(projectDir))
                break
            if ext == '.xlsx':
                count_xlsx += 1
                # name the project file
                projectFilename = name + ext
                projectFile = projectDir + '\\' + projectFilename
                # name the wx outfile
                wxFilename = name + '_wx_v1' + ext
                wxFile = projectDir + '\\' + wxFilename
        '''
        # declare arrays to hold data from the project and metadata files
        pf_headers = []
        pf_cols = []
        wx_headers = []
        wx_cols = []
        wx_hashIds = []

        # read the project and metadata files into dataframes
        df_pf = pd.read_excel(user_selected_file, sheet_name=0)
        df_meta = pd.read_excel(metaFile, sheet_name=1)

        # get the number of records in project files
        numberOfRows = len(df_pf.index)

        # get name of worksheet in the project file
        pf = pd.ExcelFile(user_selected_file)
        projectSheetName = pf.sheet_names[0]

        # copy the file headers to arrays
        for head in df_pf: pf_headers.append(head)
        for head in df_meta: wx_headers.append(head)

        # copy each column of project data as a list into an array of lists,
        # using the header array index as the iterator
        # ie: master_cols = [ [col1], [col2], [col3], ...[coln] ]
        i = 0
        for h in pf_headers:
            colname = pf_headers[i]  # get colname
            pf_cols.append(df_pf[colname])  # insert as a list to column array
            i += 1

        # create wx hash ids
        print('Creating hash ids...')
        i = 0
        while i < numberOfRows:
            hashid = hashids.encode(i)
            wx_hashIds.append(hashid)
            i += 1

        # create dictionary to hold output for new wx file
        # where key = header and val = columns
        main_dict = {}
        i = 0
        for mh in pf_headers:
            main_dict[mh] = pf_cols[i]
            i += 1
        i = 0
        for wxh in wx_headers:
            if wxh == 'wHashID':
                main_dict[wxh] = wx_hashIds
            else:
                main_dict[wxh] = ''
            i += 1

        # create pandas data frames
        df_main = pd.DataFrame(main_dict)  # main worksheet

        print('TEST -- HERE --------------')
        print(wxFilename)
        print(wxFile)

        # create excel writer
        writer = pd.ExcelWriter(wxFile)

        # write data frames to excel file
        # and skip one row to insert a user-defined header
        df_main.to_excel(writer, projectSheetName, index=False)
        writer.save()

        # end program
        print('File complete:', wxFile)

if __name__ == '__main__' : main()
