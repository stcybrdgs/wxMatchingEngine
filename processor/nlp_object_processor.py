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
            def create_nlp_pipeline(nlp)
            def modify_stop_words()
            def pickle_an_nlpobj(nobj, pname)
        # controller function
            def process_nlp_object(d)

"""
# IMPORT LIBS  =====================================
import sys
import os
import csv
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.tokens import Token
# from spacy.tokens import Span

# IMPORT PATHS  ====================================
#sys.path.append('../parameters/')
sys.path.append('../preprocessor')

# IMPORT FILES  ====================================
import loader
import string_cleaner

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
    # get the list of row heads
    row_heads = loader.get_row_heads()
    j = 0

    # normalize row heads so that they can be compared to text in nlp obj
    for rh in row_heads:
        row_heads[j] = string_cleaner.normalizer(rh)
        j += 1

    # set each row head as a sentence start
    j = 0
    for rh in row_heads:
        for token in doc:
            if token.text == rh:
                doc[token.i].is_sent_start = True
        j += 1

    return doc
    # end function //

# HELPER FUNCTIONS  ================================
def create_nlp_pipeline(nlp):
    # create custom nlp pipeline
    nlp.add_pipe(sentence_segmenter, before='ner')
    nlp.add_pipe(commonkey_tagger, before="sentence_segmenter")
    nlp.add_pipe(apply_cleanup_rules, before="commonkey_tagger")
    nlp.add_pipe(colname_tagger, before="apply_cleanup_rules")
    return nlp
    # end function//

def modify_stop_words(model):
    model.vocab[u'do'].is_stop = False
    return model
    # end function //

# store an nlp obj with a certain filename
# where arg nobj is the nlp obj
# and arg pname is the name for the pickle file
def pickle_an_nlpobj(nobj, pname):
    pass
    # end function  //

# CONTROLLER FUNCTION  =============================
def process_nlp_object(d):
    # detect language
    # need to add language detection
    # so that engine knows which model to load
    # rem 'sm' model has no word2vector capability

    # load nlp language model
    #nlp = spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm', disable=['parser'])

    # create nlp pipeline
    nlp = create_nlp_pipeline(nlp)

    # modify stop_words
    nlp = modify_stop_words(nlp)

    # create nlp obj
    nlpd = nlp(d)


    # ------------------------------------------------
    # TEST
    # ------------------------------------------------
    test(nlp, nlpd, d)

def test(nlp, nlpd, d):
    # rem d = txt obj
    # rem nlp = nlp model (en)
    # rem nlpd = nlp doc obj

    # PIPELINE
    print('\n\nHere\'s the customized NLP pipeline:')
    print(nlp.pipe_names)  # test print

    # STOP WORDS
    # show which stop words can be filtered out
    i = 0
    stops = []
    for tok in nlpd:
        if tok.is_stop:
            i += 1
            stops.append(tok.text)
    print('\nFiltered out these {} stop words: {} '.format(i, stops))

    # show the tokens that are not stop words
    #print('\nHere\'s tokens that are not stop words:')
    #tokens = [token.text for token in d if not token.is_stop]
    #print(tokens)

    # show entity labels
    print('\nHere\'s the entities text and labels:')
    ents = [(e.text, e.label_) for e in nlpd.ents]
    print(ents)

    # print row heads
    rh = loader.get_row_heads()
    print('\nHere\'s the row heads: ')
    j = 0
    for h in rh:
        print(rh[j], ' ', end='')
        j += 1

    # test the sentence segmenter
    print('\n\nSentence Segmenter:')
    for sent in nlpd.sents:
        print(sent.text, end='')

    print('\n\nSentence Segmenter (every other row):\n')
    i = 0
    for sent in nlpd.sents:
        if i % 2 == 1:
            print(sent.text, end ='')
        i += 1


    # use sentence control to print suppliers only
    print('\n\nPOS tags for first record:\n')
    i = 0
    tokens = []
    pos = []
    for sent in nlpd.sents:
        if i == 1:
            tok = [token.text for token in sent  if not token.is_stop]
            pos = [token.pos_ for token in sent if not token.is_stop]
            tag = [token.tag_ for token in sent if not token.is_stop]
            ent = [token.ent_type_ for token in sent if not token.is_stop]
        i += 1

    i = 0
    for item in tok:
        print(tok[i], pos[i], tag[i], ent[i])
        i += 1


    # COLNAME TAGGER
    #for tok in d:
    #    print(tok.text, tok.pos_, tok.tag_, tok.ent_type_)

    # COMMONKEY TAGGER


    # end function  //
