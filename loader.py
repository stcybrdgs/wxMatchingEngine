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

# PATHS ================================
sys.path.append('C:/Users/Owner/Anaconda3/Lib/site-packages')

# FUNCTIONS  =======================================
# import csv file where arg f == 'path/filename.ext'
def import_csv(d):
    pass

# import txt file based where arg f == 'path/filename.ext'
def import_txt(d):
    with open(d) as infile:
        fileObj = infile.read()
    return fileObj

# import Excel file where arg f == 'path/filename.ext'
def import_xls(d):
    pass

def loadAll():
    pass
'''
def loadDoc(d)
    loads a single document into the engine per string arg 'd'
    (where the doc is imported from either the 'io' or 'store' folders)
    and creates a doc object per one of the following options:
    #   in folder io/ the doc obj can be:   match
    #   in folder io/ the doc obj can be:   lookup, master, model , pickle , taxonomy
'''
def loadDoc(d):
    # get the path to the doc that neads to be loaded
    path = ''
    if d == 'match':
        path = '../io/input/'
    else:
        storeFolders = ['lookup', 'master', 'model', 'pickle', 'taxonomy']
        for i in storeFolders:
            if d == storeFolders[i]:
                path = '../stores/' + d + '/'

    # get the filename of the doc that needs to be loaded
    filename = os.listdir(path)

    return filename # TEST

    #filename.find(sub,start,end)
    # make sure file extension is in supported types
    # pass filename to correct import function

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
