#!/usr/bin/env python
"""
Thur Nov 14 2019
Stacy Bridges
"""
# import library components  ---------------------------------------------------
import os, shutil, sys
import pathlib
from pathlib import Path
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import unicodedata  # use to normalize international characters

# globals  ---------------------------------------------------------------------
global char_limit_for_chunker
char_limit_for_chunker = 800000 # 1166

# helper functions  ------------------------------------------------------------
def get_number_of_chunks(tender, row_num):
    global char_limit_for_chunker
    limit = char_limit_for_chunker
    num_o_chunks = 0

    char_count = 0
    for row in tender:
        row = str(row)  # eliminate any float objects
        row = unicodedata.normalize('NFKD', row).encode('ASCII', 'ignore')  # convert int'l chars
        row = row.decode('utf-8')  # convert bytes to strings
        char_count = char_count + len(row)

    product = int(char_count/limit)
    remainder = char_count % limit
    if remainder > 0:
        remainder = 1
    if char_limit_for_chunker < row_num:
        num_o_chunks = row_num
    else:
        num_o_chunks = product + remainder

    print(num_o_chunks)
    sys.exit()

    return num_o_chunks
    # end function //

def get_chunk_stop_points(chunk_num, row_num):
    stops = []
    base_stop = int(row_num/chunk_num)
    fin_stop = row_num  # base_stop + row_num % chunk_num
    stop_limit = 0
    for i in range(0,chunk_num):
        if i+1 < chunk_num:
            stop_limit = stop_limit + base_stop
        else:
            stop_limit = fin_stop
        stops.append(stop_limit)
        #print('stop: {} |  stop limit: {}'.format(i, stop_limit))
    '''
    print(base_stop, fin_stop)
    print(row_num % chunk_num)
    print(chunk_num)
    print(row_num)
    sys.exit()
    '''
    return(stops)
    # end function //

def main():
    # get input file
    folder_path = os.path.dirname(os.path.abspath(__file__))
    file_name = 'db_data_org_iesa_Conveying_memory_test.xlsx'
    infile = folder_path + '\\lib\\datafiles\\' + file_name
    col_name = 'LongText'

    # get dataframe/column
    df_tender = pd.read_excel(infile, sheet_name=0)  # read file into dataframe
    df_headers = df_tender.columns
    row_num = len(df_tender.index)
    tender = df_tender[col_name]  #mpns = df_tender['ManufacturerPartNo']

    # compute the stop points when the current chunk of data should be written
    # before moving on to the next chunk
    chunk_stop_points = []
    chunk_num = get_number_of_chunks(tender, row_num)
    must_chunk = False

    if chunk_num > 1:
        chunk_stop_points = get_chunk_stop_points(chunk_num, row_num)  # returns a list
        must_chunk = True

    print(chunk_stop_points)  # test  -------------------------

    row_count = 0
    chunk = 0
    for row in tender:
        if must_chunk == True:
            if row_count == chunk_stop_points[chunk]:
                # write chunk to temp data file
                print(row)  # print('ROW: {}, WRITE CHUNK {}({}) TO FILE'.format(row_count, chunk + 1, chunk_stop_points[chunk]))
                print('------------------------------------------------')
                chunk += 1
            else:
                print(row)
        else:
            print(row)
        row_count += 1

if __name__ == '__main__' : main()
