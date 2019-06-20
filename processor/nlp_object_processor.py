# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15
@author: Stacy Bridges

processor/
    nlp_object_processor.py
    # imports[ spacy, STOP_WORDS ]
        # custom pipes
            def colname_tagger(d)
            def remove_stop_words(d)
            def apply_cleanup_rules(d)
            def commonkey_tagger(d)
            def sentence_segmenter(d)
        # helper functions
            def modify_stop_words()
        # controller function
            def process_nlp_object(d)

"""
# IMPORT LIBS  =====================================
import sys
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# IMPORT PATHS  ====================================
#sys.path.append('../parameters/')


# IMPORT FILES  ====================================


# GLOBALS  =========================================

# CUSTOM PIPES  ====================================
def colname_tagger(doc):
    return doc
    # end function //

def apply_cleanup_rules(doc):
    return doc
    # end function //

def commonkey_tagger(doc):
    return doc
    # end function //

def sentence_segmenter(doc):
    return doc
    # end function //

# HELPER FUNCTIONS  ================================
def modify_stop_words(model):
    model.vocab[u'do'].is_stop = False
    return model
    # end function //

# CONTROLLER FUNCTION  =============================
def process_nlp_object(d):
    # need to add language detection so that engine
    # knows which model to load
    # rem 'sm' model has no word2vector capability

    # identify nlp language model
    nlp = spacy.load('en_core_web_sm')

    # modify stop_words
    nlp = modify_stop_words(nlp)

    # create custom nlp pipeline
    nlp.add_pipe(sentence_segmenter, before="parser")
    nlp.add_pipe(commonkey_tagger, before="sentence_segmenter")
    nlp.add_pipe(apply_cleanup_rules, before="commonkey_tagger")
    nlp.add_pipe(colname_tagger, before="apply_cleanup_rules")

    # create nlp obj
    d = nlp(d)

    # TEST  ------------------------------------------
    # PIPELINE
    print('\n\nHere\'s the customized NLP pipeline:\n')
    print(nlp.pipe_names)  # test print

    # STOP WORDS
    i = 0
    stops = []
    for tok in d:
        if tok.is_stop:
            i += 1
            stops.append(tok.text)
    print('\nFiltered out these {} stop words: {} '.format(i, stops), '\n')

    print(d.text)

    # show spacy stop_words
    #print('\n\nstop_words:\n')
    #print(STOP_WORDS)

    # show entity labels
    ents = [(e.text, e.label_) for e in d.ents]
    print(ents)

    # COLNAME TAGGER
    #for tok in d:
    #    print(tok.text, tok.pos_, tok.tag_, tok.ent_type_)

    # COMMONKEY TAGGER

    # SENTENCE SEGMENTER
    #print('\nHere\'s the sentence segmentation:\n')
    #for sent in d.sents:
    #    print(sent, '** end **')

    # TEST  ------------------------------------------
    # end function  //
