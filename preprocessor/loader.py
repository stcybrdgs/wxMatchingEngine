# -*- coding: utf-8 -*-
"""
Created on Thr Jun 13 14:49:44 2019
@author: Stacy Bridges

preprocessor/
    loader.py
    # imports: [ xlrd, csv, os, sys, re ]
        # helper functions
            def get_path(d)
            def get_row_heads()
            def import_json(d)
            def import_pickle(d)
            def import_xls(d)
            def import_csv(d)
            def import_txt(d)
        # controller function
            def load_doc(d)

"""
# IMPORT LIBS  ======================================
# import xlrd  # py lib for working with excel files
import csv
import os
import sys
import re

# GLOBALS  ==========================================
global row_heads
row_heads = []  # index[0] of each row for the sentence segmenter

# HELPER FUNCTIONS  =================================
# receive arg == '../path/filename.ext' and return doc obj to caller
def get_path(d):
    '''
    # get file_name, file_path, file_ext
    file = os.listdir(path)  # get ['filename'] as a list obj
    file_name = file[0]  # extract filename as str from  list obj
    file_path = path + file_name
    file_ext = file_name[file_name.find('.'):len(file_name)]
    '''
    pass
    # end function //

def get_row_heads():
    global row_heads
    return row_heads
    # end function //

def import_json(d): pass
def import_pickle(d): pass
def import_xls(d): pass

def import_txt(d):
    global row_heads
    doc = ''
    with open(d) as data:
        i = 0
        for line in data:
            j = 0
            row = line.rstrip()
            # populate row_heads[]
            id_start = j
            id_end = id_start
            for char in row:
                #if i > 0:  # skip header row
                if char == '|' and id_end == id_start:
                    id_end = j
                    row_heads.append(row[id_start:id_end])
                j += 1
            # populate txt obj
            doc = doc = doc + re.sub(r'^\s+$', '', line)
            i += 1
    return doc
    # end function //

def import_csv(d):
    global row_heads
    row_heads.clear()
    doc = ''
    with open(d) as data:
        csv_reader = csv.reader(data, delimiter='|')
        i = 0
        for row in csv_reader:
            # populate row_heads[]
            if i > 0:  # skip header row
                row_head = row[0]
                row_heads.append(row_head)
                # populate txt obj
                doc = doc + ('|'.join(row) + '\n')
            i += 1
    return doc
    # end function //

# CONTROLLER FUNCTION  =============================
# call correct import method and return doc to caller
# d == '../path/filename.ext
def load_doc(d):
    ext = d[d.rfind('.'):len(d)]
    doc = ''

    if ext == '.csv': doc = import_csv(d)
    elif ext == '.json': doc = import_json(d)
    elif ext == '.txt': doc = import_txt(d)
    elif ext == '.xls': doc = import_xls(d)

    return doc
    # end function //
