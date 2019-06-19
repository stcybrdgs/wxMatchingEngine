# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15
@author: Stacy Bridges

processor/
    processor.py
    # imports[]
        def create_nlp_object(d)
        def remove_stop_words(d)

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
# IMPORT  LIBS  ========================
import spacy
from spacy.lang.en.examples import sentences
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en.examples import sentences

# IMPORT FUNCTIONS  =====================

# GLOBALS  =========================================


# FUNCTIONS  =======================================
def create_nlp_object(d):
    # need to add language detection so that engine
    # knows which model to load
    # rem 'sm' model has no word2vector capability

    # create nlp object
    nlp = spacy.load('en_core_web_sm')
    nlp_doc = nlp(d)

    # remove stop words
    nlp_doc = nlp(remove_stop_words(nlp_doc))

    # TEST
    print('\n\nafter removing stop words: ')
    sent = nlp_doc
    print(sent.text)


# remove words from doc if they appear in stop_words.txt
def remove_stop_words(d):
    tokens =    [token.text for token in d if not token.is_stop]
    doc_string = ''
    i = 0
    for tok in tokens:
        doc_string = doc_string + ' ' + tokens[i]
        i += 1
    return doc_string
