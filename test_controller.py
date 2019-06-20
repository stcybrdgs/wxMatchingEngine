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

# GLOBALS  =========================================

# CUSTOM PIPES  ====================================
def colname_tagger(d):
    return d
    # end function //

def commonkey_tagger(d):
    return d
    # end function //

def sentence_segmenter(d):
    return d
    # end function //

# LOCAL FUNCTIONS  =================================
def remove_stop_words(d):
    tokens = [token.text for token in d if not token.is_stop]
    doc = ''
    i = 0
    for tok in tokens:
        doc = doc + ' ' + tokens[i]
        i += 1
    return doc
    # end function //

# MAIN  ============================================
def main():
    # define test input files
    f_txt = 'io/input/test/tender.txt'
    f_csv = 'io/input/test/tender.csv'

    # --------------------------------------
    # test loading and cleaning a document
    # function path: preprocessor > loader.py > load_doc(d)

    print('\nHere\'s the input doc after initial loading:\n')
    d = loader.load_doc(f_csv)
    print(d)

    print('\nHere\'s the input doc after string cleaning:\n')
    d = string_cleaner.clean_doc(d)
    print(d)

    # rem in matcher if distanceEncoder.levenshtein(d, d1) == 0 then 100% match

    # --------------------------------------
    # identify nlp language model and set up pipeline
    nlp = spacy.load('en_core_web_sm')

    # create custom nlp pipeline
    nlp.add_pipe(sentence_segmenter, before="parser")
    nlp.add_pipe(commonkey_tagger, before="sentence_segmenter")
    nlp.add_pipe(colname_tagger, before="commonkey_tagger")

    print('\n\nHere\'s the customized NLP pipeline:\n')
    print(nlp.pipe_names)  # test print



    # --------------------------------------
    # test stop words
    # function path: processor > nlp_object_processor.py > remove_stop_words(d)

    print('\nHere\'s the input doc after stop words:\n')
    nd = nlp(d)
    nd = nlp(remove_stop_words(nd))
    print(nd.text)

    print('Done')

if __name__ == '__main__' : main()
