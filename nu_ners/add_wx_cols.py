#!/usr/bin/env python
# coding: utf8
"""
Thr Oct 24, 2019
Stacy
user runs add_wxcols.py from command line
>> python add_wxcols.py
- make a copy of the project file and save with a '_wx_v1' suffix
- add the wx columns
rem xlsxwriter library docs at:
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

# main  ------------------------------------------------------------------------
def main(user_selected_file):
    print('\nAdding wx columns to \'' + user_selected_file + '\' ...')

    # define paths/names for files and directories
    mkpath = os.path.abspath(__file__)  # = (os.path.abspath('.'))
    projectDir = os.path.dirname(mkpath)
    projectSheetName = ''
    metaDir = projectDir + r'\meta'  # relative path
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

    # create dict for new wx file where key = header and val = columns
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

    # write new columns to output file
    df_main = pd.DataFrame(main_dict)  # main worksheet
    writer = pd.ExcelWriter(wxFile)  # create excel writer
    df_main.to_excel(writer, projectSheetName, index=False)  # write data frame to xlsx
    writer.save()

    # end program
    print('\nFile written')
    print(wxFilename)
    print(wxFile)

if __name__ == '__main__' : main()
