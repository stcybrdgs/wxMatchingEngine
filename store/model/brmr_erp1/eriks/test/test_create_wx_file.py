#!/usr/bin/env python
# coding: utf8
"""
Friday Aug 16, 2019
Stacy Bridges

create_w_file.py

- pick up a new client .xls file
- add wx columns
- add unique hashids
- save as wx .xlsx file

"""
import os
import pathlib
from pathlib import Path
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# manually set i/o files
masterfile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\master\Data for Test MR 13082019.xlsx'
mastersheet = 'Sheet1'
wxmdfile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\inputs\wx_metadata.xlsx'  # wxmetadata
wxmdsheet = 'WrWx Fields'
outfile = 'Data for Test MR 13082019_wx.xlsx'

'''
# read the xlsx input file
df = pd.read_excel(masterfile, sheet_name='Sheet1')

# print out the column headings as a list
print("Column headings:")
print(df.columns)

# print out column headings as rows
fields = []
for col in df:
    print(col)
    fields.append(col)

# print all rows as a column, with schema info
for f in fields:
    print(df[f])

# save entire column into a list
col1 = []
col1 = df[fields[0]]
print('Col 1, Row 1:', col1[0])

# count number of columns
count = 0
for col in df:
    count += 1

print('Number of cols: ', count)

# extract filename from path
print(os.path.basename('../master/text.txt'))
print(os.getcwd())
print(os.listdir('eriks/'))
'''

# build wx file  -----------------------------------
master_headers = []
master_cols = []
wx_headers = []
#wx_cols = []

# read master master file & wx_metadata file
df_master = pd.read_excel(masterfile, sheet_name=mastersheet)
df_wxmd = pd.read_excel(wxmdfile, sheet_name=wxmdsheet)

# copy headers to arrays
for col in df_master: master_headers.append(col)
for col in df_wxmd: wx_headers.append(col)

# copy columns as lists into arrays of lists
# ie: master_cols = [ [col1], [col2], [col3], ...[coln] ]
# using header array index as counter
i = 0
for h in master_headers:
    colname = master_headers[i]  # get colname
    master_cols.append([ df_master[colname] ])  # insert as a list to column array
    i += 1

# add headers

# add summary tab

# add definitions tab

# add wrwx hash ids

# tester
print(master_headers)
print(wx_headers)
