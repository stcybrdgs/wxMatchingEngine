# -*- coding: utf-8 -*-
"""
Created on Thr Jun 13 14:49:44 2019
@author: Stacy Bridges

"""

# IMPORTS  =========================================
import csv
import xlrd


# FUNCTIONS  =======================================
# import csv file where arg f == 'path/filename.ext'
def import_csv(f):
    pass

# import txt file based where arg f == 'path/filename.ext'
def import_txt(f):
    with open(f) as infile:
        fileObj = infile.read()
    return fileObj

# import Excel file where arg f == 'path/filename.ext'
def import_xls(f):
    pass

def loadAll():
    pass

# load a single document into the engine as determined by
# the single passed-in argument representing which doc to import:
#   lookup, master, model , pickle , taxonomy
def loadDoc(d):
        # detect docs
    # choose import function depending on doctype


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

    pass
