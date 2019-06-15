# -*- coding: utf-8 -*-
"""
Created on Thr Jun 13 14:49:44 2019
@author: Stacy

methods for first run of the NERS Tester
    test_NERS_loader()
    test_NERS_preProcessor()
	test_NERS_trainer()
	test_NERS_matcher()

test/

"""

# IMPORTS  =========================================
import csv

# FUNCTIONS  =======================================
def test_NERS_loader(doc):
    # rem at the head of this function, use os and sys
    # to detect files that need to be imported

    # load taxonomies  -------------------------
    # (future spring loads taxonomies based on market domain)
    #   tx_bearings = nlp(f1)  # taxonomies/bearings.json
    #   tx_pumps = nlp(f2)  # taxonomies/pumps.json
    if doc == 'txb':
        print('The Bearing Taxonomy is disconnected...')  # tax_brng
        return ''

    elif doc == 'txp':
        print('The Pump Taxonomy is disconnected...')  # tax_pmp
        return ''


    # load lookups  ------------------------------
    # (future sprint loads lookups based on target master)
    #   lk_suppliers = nlp(f3)  # lookups/bhSuppliers.json
    elif doc == 'lk':
        print('The Suppliers Lookup is disconnected...')  # lookup
        return ''


    # load models   -------------------------------
    # rem only one master per run
    # rem for test, use erp
    #   md_erp = nlp(f4)  # models/erp10.csv
    elif doc == 'erp':
        print('Loading the ERP master...')  # erp
        # stubbing in exerpts from the erp file:
        '''
        # data stub:
        row1 = '104A2102,Plummer Block Housing,SKF,SE511-609K7,Bolt Hole Centre Distances 2100 MM | Height Centre 700 MM | Net Weight 95.46 KG'
        row2 = '45026245,Plummer Block Housing,SKF,SE509,Bolt Hole Centre Distances 210 MM | Height Centre 70 MM | Net Weight 5.46 KG'
        row3 = '104A2394,Plummer Block Housing,SKF,SE510-608,Bolt Hole Centre Distances 150 MM | Height Centre 60 MM | Net Weight 2.53 KG'
        # concatenate rows to create doc
        erpDoc = row1 + '\n' + row2 + '\n' + row3
        '''
    	# read file into string object
        '''
        inFile = open('../stores/models/erp10.csv', 'rt')
        erpDoc = inFile.read()
        inFile.close()
        '''
        infile = '../stores/models/erp10.csv'
        outfile = '../io/output/erp10_output.csv'
        with open(infile, 'rt') as f:
            erpDoc = csv.reader(f)
        '''
        # write contents of string object to io output folder
        g = open(outfile, 'wt')
        for line in erpDoc:
            g.writeline(line)
            #print(end='', flush=True) # rem flush the output buffer
        '''
        f.close()
        #g.close()

        # return object to caller
        return erpDoc

    # load pickles  -------------------------------
    elif doc == 'pkl':
        print('Loading pickled stores...')  # pickle


    # load match docs  -------------------------
    # rem only one match doc per run
    # for test, use tender
    #   tender = nlp(f5)  # io/input/tender.csv
    elif doc == 'tdr':
        print('Loading the Tender...')  # tender
        inFile = open('../stores/models/erp10.csv', 'r')
        tdrDoc = inFile.read()
        inFile.close()
        return tdrDoc

def test_NERS_preProcessor():
    print('Running The Pre-Processor...')

def test_NERS_trainer():
    print('Running The NERS Trainer...')

def test_NERS_matcher():
    print('Running The NERS Matcher...')