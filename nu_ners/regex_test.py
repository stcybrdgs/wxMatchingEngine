"""
Thur Oct 31, 2019
Stacy Bridges

"""
import re, os, sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

# get input file
folder_path = os.path.dirname(os.path.abspath(__file__))
infile = folder_path + '\\db_data_org_electrical_short_wx_v1.xlsx'
outfile = folder_path + '\\api_in_ids.csv'

# get dataframe/column
df_tender = pd.read_excel(infile, sheet_name=0)  # read file into dataframe
mpns = df_tender['ManufacturerPartNo']

# identify search pattern
RS_regex='\d{3}[-]\d{3,4}'

# print search results to console
results = []
for row in mpns:
    results.append(re.findall(RS_regex,str(row)))
with open(outfile, 'w') as ofile:
    ofile.write('RS Code')
    ofile.write('\n')
    id_count = 0
    for i in results:
        if len(i)>0:
            id_count += 1
            print(i[0])
            ofile.write(i[0])
            ofile.write('\n')
        else:
            ofile.write('\n')

print('{} codes extracted and written to:'.format(id_count))
print(outfile)
