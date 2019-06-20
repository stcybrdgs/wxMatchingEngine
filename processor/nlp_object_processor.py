# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15
@author: Stacy Bridges

processor/
    processor.py
    # imports[ spacy, STOP_WORDS ]
        # custom pipes
            def colname_tagger(d)
            def commonkey_tagger(d)
            def sentence_segmenter(d)
        # helper functions
            def remove_stop_words(d)
        # controller function
            def process_nlp_object(d)

"""
# IMPORT LIBS  =====================================
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# IMPORT PATHS  ====================================

# IMPORT FUNCTIONS  ================================

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

# HELPER FUNCTIONS  ================================
def remove_stop_words(d):
    tokens = [token.text for token in d if not token.is_stop]
    doc = ''
    i = 0
    for tok in tokens:
        doc = doc + ' ' + tokens[i]
        i += 1
    return doc
    # end function //

# CONTROLLER FUNCTION  =============================
def process_nlp_object(d):
    # need to add language detection so that engine
    # knows which model to load
    # rem 'sm' model has no word2vector capability

    # identify nlp language model
    nlp = spacy.load('en_core_web_sm')

    # create custom nlp pipeline
    nlp.add_pipe(sentence_segmenter, before="parser")
    nlp.add_pipe(commonkey_tagger, before="sentence_segmenter")
    nlp.add_pipe(colname_tagger, before="commonkey_tagger")

    # create nlp obj
    d = nlp(d)

    # remove stop words
    d = nlp(remove_stop_words(d))

    # TEST  ------------------------------------------
    print('\n\nHere\'s the customized NLP pipeline:\n')
    print(nlp.pipe_names)  # test print

    print('\nHere\'s the input doc after stop words:\n')
    print(d.text)
    # TEST  ------------------------------------------
    # end function  //
