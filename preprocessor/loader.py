# -*- coding: utf-8 -*-
"""
Created on Thr Jun 13 14:49:44 2019
@author: Stacy Bridges

"""

# IMPORTS  =========================================
import csv
# import xlrd # need to put library in local folder for detection
import os
import sys


# FUNCTIONS  =======================================
# receive arg == 'path/filename.csv' and
# return doc obj to caller
# (works with Excel-generated csv files)
# (needs pipe delimiter)
def import_csv(d):
    with open(d) as infile:
        fileObj = csv.reader(infile, delimiter='|')
        doc = ''
        for row in fileObj:
            print(row)
            
    return doc
    # print('import_csv: ' + d)

# receive arg == 'path/filename.json' and
# return doc obj to caller
def import_json(d):
    # TEST
    print('import_json: ' + d)

# receive arg == 'path/filename.pickle' and
# return doc obj to caller
def import_pickle(d):
    # TEST
    print('import_pickle: ' + d)

# receive arg == 'path/filename.txt' and
# return doc obj to caller
def import_txt(d):
    with open(d) as infile:
        fileObj = infile.read()
    return fileObj

# receive arg == 'path/filename.xls' and
# return doc obj to caller
def import_xls(d):
    # TEST
    print('import_xls: ' + d)
    pass

# function description
def load_all():
    pass

# load a doc per arg whose value is an index in
# ['mark', 'lookup', 'master', 'model', 'pickle', 'taxonomy']
def loadDoc(d):
    # get the path to the doc that neads to be loaded
    path = ''
    if d == 'mark':
        path = '../io/input/mark/'
    else:
        storeFolders = ['lookup', 'master', 'model', 'taxonomy']
        for i in storeFolders:
            if d == i:
                path = '../stores/' + d + '/'

    # get file_name, file_path, file_ext
    file = os.listdir(path)  # get ['filename'] as a list obj
    file_name = file[0]  # extract filename as str from  list obj
    file_path = path + file_name
    file_ext = file_name[file_name.find('.'):len(file_name)]

    # call the import method that's appropriate for the file .ext
    # and return a doc obj to the caller
    docObj =''
    if file_ext == '.csv':
        docObj = import_csv(file_path)
    elif file_ext == '.json':
        docObj = import_json(file_path)
    elif file_ext == '.txt':
        docObj = import_txt(file_path)
    elif file_ext == '.xls':
        docObj = import_xls(file_path)

    # TEST ----------------------------------------------------
    #print(docObj[0:100])
    print(docObj)
    print('{}, {}, {}'.format(file_path, file_name, file_ext))
    return docObj  # use list indexing to return 'filename'
    # ---------------------------------------------------------


    # lookup

    # load taxonomies  -------------------------
    # (future spring loads taxonomies based on market domain)
    #   tx_bearings = nlp(f1)  # taxonomies/bearings.json
    #   tx_pumps = nlp(f2)  # taxonomies/pumps.json

    # load lookups  ------------------------------
    # (future sprint loads lookups based on target master)
    #   lk_suppliers = nlp(f3)  # lookups/bhSuppliers.json

    # load models   -------------------------------
    # rem only one master per run
    # rem for test, use erp
    #   md_erp = nlp(f4)  # models/erp10.csv

    # load pickles  -------------------------------

    # load match docs  -------------------------
    # rem only one match doc per run
    # for test, use tender
    #   tender = nlp(f5)  # io/input/tender.csv
