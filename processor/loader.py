# -*- coding: utf-8 -*-
"""
Created on Thr Jun 13 14:49:44 2019
@author: Stacy

load files to be used by the nlp processor:
    - stores
        - taxonomies
        - lookups (suppliers, etc)
        - models
            - master docs (mdm, erp, etc)
        - pickles
    - io
        - match docs (tenders, etc)

processor/

"""

# IMPORTS  =========================================



# FUNCTIONS  =======================================
def loadAll():
    pass

# load a single document into the engine as determined by
# the single passed-in argument
def loadDoc(d):
    '''
    lookup
    master
    model
    pickle
    taxonomy


    '''
    print('Running the loader...')

    if d == 'tx':
        print('taxonomy doc loaded.')
    elif d == 'lk':
        print('lookup doc loaded.')
    elif d == 'erp':
        print('erp doc loaded.')
    elif d == 'tdr':
        print('tender doc loaded.')

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
