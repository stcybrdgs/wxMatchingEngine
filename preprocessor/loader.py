# -*- coding: utf-8 -*-
"""
Created on Thr Jun 13 14:49:44 2019
@author: Stacy Bridges

preprocessor/
    loader.py
    # imports: [ xlrd, csv, os, sys, re ]
        # helper functions
            def get_path(d)
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

def import_json(d): pass
def import_pickle(d): pass
def import_xls(d): pass

def import_txt(d):
    doc = ''
    with open(d) as data:
        for row in data:
            # regex removes blank lines
            doc = doc + re.sub(r'^\s+$', '', row)
    return doc
    # end function //

def import_csv(d):
    doc = ''
    with open(d) as data:
        csv_reader = csv.reader(data, delimiter='|')
        for row in csv_reader:
            doc = doc + ('|'.join(row) + '\n')
    return doc
    # end function //

# CONTROLLER FUNCTION  =============================
# call correct import method and return doc to caller
# d == '../path/filename.ext
def load_doc(d):
    ext = d[d.find('.'):len(d)]
    doc =''

    if ext == '.csv': doc = import_csv(d)
    elif ext == '.json': doc = import_json(d)
    elif ext == '.txt': doc = import_txt(d)
    elif ext == '.xls': doc = import_xls(d)

    return doc
    # end function //
