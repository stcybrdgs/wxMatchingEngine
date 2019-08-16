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
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# manually set i/o files
infile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\Data for Test MR 13082019.xlsx'
outfile = 'Data for Test MR 13082019_wx.xlsx'

# read the xlsx input file
df = pd.read_excel(infile, sheet_name='Sheet1')

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

# add headers
