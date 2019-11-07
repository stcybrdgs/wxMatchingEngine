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

    # store each wBrand_all record as a string in a new array
    brand_rows = []
    for row in wBrand_all:
        if str(row) == 'nan': row = ''  # store each empty record as ''
        else: row = str(row) + ','  # append ',' to each row to allow for tokenizing
        brand_rows.append(row)  # store each row in the list of rows

    # convert each string in the array into a list of tokens
    # ie, ['SKF, COOPER, SMC', 'RS, TIMKEN'] becomes
    #     [ ['SKF', 'COOPER', 'SMC'], ['RS', 'TIMKEN'] ]
    # rem by tokenizing the substrings in this way, the brands can be indexed
    # and operated upon (ie count(), sum(), etc.)
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
        brand_rows[i] = (tokens[:])
        tokens.clear()
        i += 1

    # filter off only the unique brands into a separate array
    unique_brands = []  # this array is parallel to unique_brands_count[]
    unique_brands_counts = []  # this array is parallel to unique_brands[]
    brand_tot_count = 0
    brand_unique_count = 0
    for list in brand_rows:
        for item in list:
            brand_tot_count += 1  # get the count of total brands
            if item not in unique_brands:
                # store name of unique brand
                unique_brands.append(item)
                # store a placeholder for how many times each unique brand appears in the data
                # ...will get actual value below **
                unique_brands_counts.append(0)
    brand_unique_count = len(unique_brands)  # the count of unique brands

    # **find out how many times each unique brand appears in the data
    for list in brand_rows:
        for item in list:
            i = 0
            for unique_item in unique_brands:
                if item == unique_item:
                    unique_brands_counts[i] = unique_brands_counts[i] + 1
                    break
                i += 1

    # get the primary brand for each record
    wBrand_prim = []
    brand_names_in_list = []
    brand_counts_in_list = []
    for list in brand_rows:
        j = 0
        for item in list:
            k = 0:
            for unique_item in unique_brands:
                if item == unique_item:
                    brand_names_in_list.append(item)
                    brand_counts_in_list.append(unique_brands_counts[k])
                    break
                k += 1  # inc unique_item in unique_brands
            j += 1  # inc item in list
        # maxval = max val in brand_counts_in_list
        # index = index of max val in brand_counts_in_list
        # wBrand_prim.append(brand_names_in_list[index])

    # prepare pandas data frame for output file where
    # {'wBrand_prim':wBrand_prim}



    # TEST  --------------------------------------------------------------------
    print('{} total, {} unique'.format(brand_tot_count, len(unique_brands)))
    i = 0
    for ub in unique_brands:
        ubcount = unique_brands_counts[i]
        print('{} | {}'.format(ub, ubcount))
        i += 1

    # end program
    print('Done.')

if __name__ == '__main__' : main()
