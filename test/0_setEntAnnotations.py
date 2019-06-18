# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18
@author: Stacy Bridges

script to set entity annotations
"""

# IMPORT LIBS  ======================================
import spacy
from spacy.tokens import Span
import csv
import sys
import os

# PATHS ================================
sys.path.append('../preprocessor/')

# IMPORT FUNCTIONS  =====================
import preprocessor

# GLOBALS  ==============================

# CUSTOM PIPES  =========================
def custom_sentencizer(doc):
    for i, token in enumerate(doc[:-2]):
        # Define sentence start if pipe + titlecase token
        if token.text == "|" and doc[i+1].is_title:
            doc[i+1].is_sent_start = True
        else:
            # Explicitly set sentence start to False otherwise, to tell
            # the parser to leave those tokens alone
            doc[i+1].is_sent_start = False
    return doc

def common_key_tagger(doc):
    print("After tokenization, this doc has {} tokens.".format(len(doc)))
    print("The part-of-speech tags are:", [token.pos_ for token in doc])
    if len(doc) < 10:
        print("This is a pretty short document.")
    return doc

# MAIN  =======================================
def main():
    # get english language model
    # and remove the dependency-parcing pipeline
    nlp = spacy.load('en_core_web_sm', disable=['parser'])

    # want to add custom pipe components to create the following pipeline:
    # tokenizer -> tagger -> custom_sentencizer -> ner -> common_key_tagger
    # consider adding: entity_ruler, merge_noun_chunks (https://spacy.io/usage/processing-pipelines/)
    nlp.add_pipe(custom_sentencizer, before="ner")  # Insert before the parser
    nlp.add_pipe(common_key_tagger, name="common_key_tagger", last=True)
    print(nlp.pipe_names)

    # get product group data file
    txt_obj = ''
    with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as data:
        data = csv.reader(data, delimiter='|')
        i = 0
        for row in data:
            # create text object with '.' at end
            if i != 0:
                txt_obj = txt_obj + ' '.join(row) + '.\n'
            i += 1

    print('\n\n', txt_obj)
    nlp_obj = nlp(txt_obj)
    print('\n\n')
    i = 0
    for sent in nlp_obj.sents:
        print(sent.text, '**end**')
        i += 1
    print('\n\n# of sents: ', i)

    # observations:
    # if you don't clean the txt_obj, spacy sees all records as one sentence

    # clean the text object
    txt_obj = preprocessor.string_cleaner(txt_obj)

    # TEST PRINT  -----------------------
    print('\n\ntxt_obj after cleaning:\n', txt_obj)

    # create the nlp object:
    nlp_obj_cln = nlp(txt_obj)
    print('\n\ntxt_obj_cln:\n')

    # TEST print  -----------------------
    i = 0
    for sent in nlp_obj_cln.sents:
        print(sent.text, '**end**')
        i += 1
    print('\n\n# of sents: ', i)

    #--------------------------------------
    # testing: setting entity annotations
    #--------------------------------------
    ents = [(e.text, e.start_char, e.end_char, e.label_) for e in nlp_obj_cln.ents]
    print('\nBefore', ents)
    # the model didn't recognise "FB" as an entity :(

    # find token positions
    print('\n\nfind token positions:\n')
    for token in nlp_obj_cln:
        print(token.text, token.i)

    PRODUCT = nlp_obj_cln.vocab.strings[u"PRODUCT"]
    # get hash value of entity label
    igp = Span(nlp_obj_cln, 1, 4, label=PRODUCT) # create a Span for the new entity
    nlp_obj_cln.ents = list(nlp_obj_cln.ents) + [igp]

    ents = [(e.text, e.start_char, e.end_char, e.label_) for e in nlp_obj_cln.ents]
    print('\nAfter', ents)

    for e in nlp_obj_cln.ents:
        if e.text == 'internal gear pump':
            print(e.text, ' is a ', e.label_)

if __name__ == '__main__' : main()
