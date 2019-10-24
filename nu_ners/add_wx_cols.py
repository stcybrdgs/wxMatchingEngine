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
import os
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

# start program
print('Adding wx fields...')

# define paths/names for files and directories
mkpath = os.path.abspath(__file__)  # = (os.path.abspath('.'))
projectDir = os.path.dirname(mkpath)
templateDir = os.path.dirname(projectDir) + r'\NERS_Template'  # relative path
nersDir = projectDir + r'\ners'
projectFile = ''
projectFilename = ''
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
print('mkpath:', mkpath)
print('projectDir:',projectDir)
print('templateDir:',templateDir)
print('nersDir:',nersDir)
print('wxFilename:', wxFilename)
print('wxFile:', wxFile)
'''

# only create transformed wx file if exactly one project file exists in folder
if count_xlsx <= 1:
    if count_xlsx == 0:
        # throw an error if there is no project file
        print('Error: There must be one .xlsx file at the base of {}'.format(projectDir))
    else:
        # declare arrays to hold data from the project and metadata files
        pf_headers = []
        pf_cols = []
        wx_headers = []
        wx_cols = []
        wx_hashIds = []

        # read the project and metadata files into dataframes
        df_pf = pd.read_excel(projectFile, sheet_name=0)
        df_meta = pd.read_excel(metaFile, sheet_name=1)

        # get the number of records in project files
        numberOfRows = len(df_pf.index)

        # get name of worksheet in the project file
        pf = pd.ExcelFile(projectFile)
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

        # create excel writer
        writer = pd.ExcelWriter(wxFile)

        # write data frames to excel file
        # and skip one row to insert a user-defined header
        df_main.to_excel(writer, projectSheetName, index=False)
        writer.save()

        # test  ----------------------------------------------------------------
        #'''
        print('mkpath:\t\t\t{}\nprojectDir:\t\t{}\nnersDir:\t\t{}\ntemplateDir:\t\t{}\nmetaDir:\t\t{}\nmetaFile:\t\t{}\nprojectFile:\t\t{}\nprojectFilename:\t{}\nwxFile:\t\t\t{}'.format(
            mkpath, projectDir, nersDir, templateDir, metaDir, metaFile, projectFile, projectFilename, wxFile))
        print('pf_headers:', pf_headers)
        print('wx_headers:', wx_headers)
        print('projectSheetName:', projectSheetName)
        print('pf_headers:', pf_headers)
        print('wx_headers:', wx_headers)
        print('number of rows:', numberOfRows)
        print('number of pf headers:', len(pf_headers))
        #'''

# end program
print('File complete:', wxFile)
print('Done.')
