# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15
@author: Stacy Bridges

processor/
    processor.py
    # imports[ spacy, STOP_WORDS ]
        def create_nlp_object(d)
        def remove_stop_words(d)

"""
# IMPORT LIBS  =====================================
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# CUSTOM PIPES  ====================================
def remove_stop_words(d):
    tokens = [token.text for token in d if not token.is_stop]
    doc = ''
    i = 0
    for tok in tokens:
        doc = doc + ' ' + tokens[i]
        i += 1
    return doc
    # end function //
    
# HELPER FUNCTIONS  ================================


# CONTROLLER FUNCTION  =============================
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
    # end function //
