# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15
@author: Stacy Bridges

processor/
    processor.py
    # imports[]
        def create_nlp_object(d)


"""
# IMPORT  LIBS  ========================
import spacy
from spacy.lang.en.examples import sentences

# IMPORT FUNCTIONS  =====================
import preprocessor

# GLOBALS  =========================================


# FUNCTIONS  =======================================
def create_nlp_object(d):
    # need to add language detection so that engine
    # knows which model to load
    # rem 'sm' model has no word2vector capability

    # create nlp object
    nlp = spacy.load('en_core_web_sm')
    nlp_obj = nlp(d)

    # groom stop words out of nlp object
    nlp_obj = preprocessor.remove_stop_words(nlp_obj)

    # TEST
    print(nlp_obj.text)
    '''
    for token in nlp_obj:
        print(token.text)
    '''


    # how do you pass nlp objects?
