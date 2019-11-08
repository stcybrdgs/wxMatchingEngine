"""
Thur Nov 7, 2019
Stacy Bridges

This script searches through a user-selected column of input data to extract
regex patterns resembling RS product codes. The results are printed to the
console and also written back to the project file that contains the original
column of input data. The output is written to a column called RS_Codes.

"""
# import libraries  ------------------------------------------------------------
import re, os, sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

# main  ------------------------------------------------------------------------
# get input file
folder_path = os.path.dirname(os.path.abspath(__file__))
infile = folder_path + '\\db_data_org_electrical_nutest_wx_v1.xlsx'
outfile = folder_path + '\\api_in_ids.csv'

# get dataframe/column
df_tender = pd.read_excel(infile, sheet_name=0)  # read file into dataframe
mpns = df_tender['Description']  #mpns = df_tender['ManufacturerPartNo']

# identify regex search patterns
rs_regex_1='[\s,({[]\d{3}[-]\d{3,4}[\s,)}]'  # case 1: the regex is inline
rs_regex_2='^\d{3}[-]\d{3,4}[\s,)}]'  # case 2: the regex is at start of line
rs_regex_3='[\s,({[]\d{3}[-]\d{3,4}$'  # case 3: the regex is at end of line

# find rs codes per regex rules
results = []
for row in mpns:
    results.append(re.findall(rs_regex_3,str(row)))

# strip leading and trailing chars from result strings
lead_trail_chars = [' ', ',', '(', '{', '[', ')', '}', ']']
final_codes = []
for list in results:
    if len(list) > 0:
        for string in list:
            token = ''
            #if len(string) > 0:
            for char in string:
                if char not in lead_trail_chars:
                    token = token + char
            final_codes.append(token)
    else:
        final_codes.append('')

# print final codes to outfile and console
with open(outfile, 'w') as ofile:
    ofile.write('RS Code')
    ofile.write('\n')
    id_count = 0
    for item in final_codes:
        if len(item)>0:
            id_count += 1
            print(item)
            ofile.write(item)
            ofile.write('\n')
        else:
            ofile.write('\n')

print('{} codes extracted and written to:'.format(id_count))
print(outfile)
