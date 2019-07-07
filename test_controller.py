# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19
@author: Stacy Bridges

# TO DO:
# tagger: lu token vs span vs ent -- which tag to use for which data?
#   Product ID, Product, Supplier, MfrPartNo, Description
#       ent: PRODUCT (token level), tok: soundex, tok NYSIIS
#       ent: SUPPLIER (token level), tok: soundex, tok NYSIIS
#       ent: PRODUCT_ID (token level)
#       ent: MPN (token level)
#       span: DESCRIPTION [x:x]
#   pos == noun for chunking (?)
#       if find( inProduct, isName) >= 0 where isName in [ taxonomy ]:
#           cat(noun | noun | noun) = chunk = name of chunk
#  tagger.add.label --> add new label to the pipe (can map a dictionary)

"""
# IMPORT LIBS  =====================================
import csv
import sys
import os
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.tokens import Token

# from spacy.lang.en.stop_words import STOP_WORDS

# IMPORT PATHS  ====================================
sys.path.append('io/')
sys.path.append('ners/')
sys.path.append('preprocessor/')
sys.path.append('processor/')
sys.path.append('store/')

# IMPORT FUNCTIONS  ================================
import loader
import string_cleaner
import processor
import distance_encoder
import nlp_object_processor

# GLOBALS  =========================================

# MAIN  ============================================
def main():
    # define test input files
    tender_txt = 'io/input/marq/tender.txt'
    tender_csv = 'io/input/marq/tender.csv'
    erp_csv = 'io/input/test/erp10_master.csv'

    # --------------------------------------
    # test loading and cleaning a document
    # function path: preprocessor > loader.py > load_doc(d)

    print('\nHere\'s the input doc after initial loading:\n')
    d = loader.load_doc(tender_csv)
    print(d)

    print('\nHere\'s the input doc after string cleaning:\n')
    d = string_cleaner.clean_doc(d)
    print(d)

    # rem in matcher if distanceEncoder.levenshtein(d, d1) == 0 then 100% match

    # send object to the nlp object processor
    nlp_object_processor.process_nlp_object(d)

    # end program
    print('\nDone')

if __name__ == '__main__' : main()
