#!/usr/bin/env python
# coding: utf8
"""
Thur, Nov 7, 2019
Stacy Bridges

Selects the primary brand for each record:
- if wBrand_all == '', primary brand == ''
- if wBrand_all count == 1, primary brand == wBrand_all
- if wBrand_all count > 1:
    - for each brand b in the wBrand_all field, count each time it occurs in the column
    - then, primary brand == max [b1_count, b2_count, ..., bn_count]
- if wBrand_prim column was previously populated, overwrite it each time new values
  are determined

"""
import pandas as pd
from pandas import ExcelWriter
import numpy as np

def main():
    user_selected_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners_v2\ners\db_data_org_electrical_short_wx_v1.xlsx'

    # read the project and metadata files into dataframes
    df = pd.read_excel(user_selected_file, sheet_name=0)
    wBrand_all = df['wBrand_all']
    wBrand_prim = df['wBrand_prim']

    # store each wBrand_all record in a new list
    brand_rows = []
    for row in wBrand_all:
        if str(row) == 'nan': row = ''  # store each empty record as ''
        else: row = str(row) + ','  # append ',' to each row to allow for tokenizing
        brand_rows.append(row)  # store each row in the list of rows

    # tokenize each row and store each row as a list of tokens
    tokens = []
    token = ''
    start_loc = 0  # start of token
    comma_loc = 0  # end of token
    i = 0
    for row in brand_rows:
        comma_loc = row.find(',')  # end of token
        while comma_loc >= 0:
            token = row[start_loc:comma_loc]
            tokens.append(token)
            row = row[comma_loc+2:len(row)]  # truncate row string by length of token
            comma_loc = row.find(',')  # reset token ending loc
        print(tokens)
        brand_rows[i] = (tokens[:])
        tokens.clear()
        i += 1

    for list in brand_rows:
        print(list)

    # end program
    print('Done.')

if __name__ == '__main__' : main()
