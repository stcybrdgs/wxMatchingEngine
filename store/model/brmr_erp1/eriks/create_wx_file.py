#!/usr/bin/env python
# coding: utf8
"""
Friday Aug 16, 2019
Stacy Bridges

create_w_file.py
- import the client file
- add wx columns, unique ids, summary tab, & definitions tab
- export the cleaned WrWx .xlsx file

"""
import os
import pathlib
from pathlib import Path
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# manually set i/o file name and worksheet name  -------------------------------
masterfile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\master\Data for Test MR 13082019.xlsx'
mastersheet = 'Sheet1'

#  -----------------------------------------------------------------------------

# generate names for output files and worksheets
masterfile_basename = os.path.basename(masterfile)
mastertab = masterfile_basename[0:len(masterfile_basename)-5]
projectpath = masterfile[0:masterfile.find('master')]
wxmdfile = projectpath + r'input\wx_metadata.xlsx'  # wxmetadata
wxmdsheet = 'WrWx Fields'
outfile = projectpath + r'\output\\' + mastertab + '_wx.xlsx'

# build wx file  -----------------------------------
master_headers = []
master_cols = []
wx_headers = []
wx_cols = []

# read master master file & wx_metadata file
df_master = pd.read_excel(masterfile, sheet_name=mastersheet)
df_wxmd = pd.read_excel(wxmdfile, sheet_name=wxmdsheet)

# copy headers to arrays
for col in df_master: master_headers.append(col)
for col in df_wxmd: wx_headers.append(col)

# copy cols as lists into arrays of lists using header array index as counter
# ie: master_cols = [ [col1], [col2], [col3], ...[coln] ]
i = 0
for h in master_headers:
    colname = master_headers[i]  # get colname
    master_cols.append(df_master[colname])  # insert as a list to column array
    i += 1

# add summary tab

# add definitions tab

# add wrwx hash ids

# create dictionary for main worksheet in output file
main_dict = {}
i = 0
for mh in master_headers:
    main_dict[mh] = master_cols[i]
    i += 1
i = 0
for wxh in wx_headers:
    main_dict[wxh] = ''
    i += 1

# tester
print(master_headers, '\n', wx_headers)

# create pandas data frames
#df_summary = pd.DataFrame(summary_dict)  # summary worksheet
df_main = pd.DataFrame(main_dict)  # main worksheet
#df3_defs = pd.DataFrame(def_dict)  # col defs worksheet

# create excel writer
writer = pd.ExcelWriter(outfile)

# write data frames to excel file
#df_summary.to_excel(writer, 'Summary', index=False)
df_main.to_excel(writer, mastertab, index=False)
#df_defs.to_excel(writer, 'WrWx Field Definitions', index=False)
writer.save()
