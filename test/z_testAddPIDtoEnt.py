# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18
@author: Stacy Bridges

script to test adding ent tag to product ids
"""

# IMPORT LIBS  ======================================
import spacy
from spacy.tokens import Span
from spacy.strings import StringStore
import csv
import sys
import os

# PATHS ================================
sys.path.append('../preprocessor/')

# IMPORT FUNCTIONS  =====================
import preprocessor

# GLOBALS  ==============================
global product_ids
product_ids = []

# CUSTOM PIPES  =========================
def common_key_tagger(doc):
    #print("After tokenization, this doc has {} tokens.".format(len(doc)))
    #print("The part-of-speech tags are:", [token.pos_ for token in doc])
    if len(doc) < 10:
        #print("This is a pretty short document.")
        pass
    return doc

def custom_sentencizer(doc):
    pass
    return doc
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

# MAIN  =======================================
def main():
    # get english language model
    # and remove the dependency-parcing pipeline
    nlp = spacy.load('en_core_web_sm')#, disable=['parser'])

    # want to add custom pipe components to create the following pipeline:
    # tokenizer -> tagger -> custom_sentencizer -> ner -> common_key_tagger
    # consider adding: entity_ruler, merge_noun_chunks (https://spacy.io/usage/processing-pipelines/)
    nlp.add_pipe(custom_sentencizer, before="tagger")  # Insert before the parser
    #nlp.add_pipe(field_val_tagger, name = "field_val_tagger", last=True)
    nlp.add_pipe(common_key_tagger, name="common_key_tagger", last=True)

    print(nlp.pipe_names)  # test print

    # get product group data file
    txt_obj = ''
    with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as data:
        data = csv.reader(data, delimiter='|')
        i = 0
        header = []
        global product_ids
        for row in data:
            if i == 0:
                header.append(row)
            else:
                # rem string.cleaner normalized all text in text obj
                # so all metadata must also be normalized to enable
                # matching
                product_id = row[0].lower()
                product_ids.append(product_id)
            # create text object with '.' at end
            if i != 0:
                txt_obj = txt_obj + ' '.join(row) + '.\n'
            i += 1

    # print('\n\n# of sents: ', i)  # test print
    print('\n\ncontents of header and product_ids[]:\n')
    print(header)
    print(product_ids)

    # clean the text object
    txt_obj = preprocessor.string_cleaner(txt_obj)

    # create NLP object  ----------------------
    # print('\n\n', txt_obj)  # test print
    nlp_obj = nlp(txt_obj)
    print('\n\n')  # test print
    i = 0
    for sent in nlp_obj.sents:
        print(sent.text, '**end**')
        i += 1



    #--------------------------------------
    # testing: setting entity annotations
    #--------------------------------------
    '''
    # find token positions
    print('\n\nfind token positions:\n')
    for token in nlp_obj:
        print(token.text, token.i)

    PRODUCT = nlp_obj.vocab.strings[u"PRODUCT"]
    # get hash value of entity label
    igp = Span(nlp_obj, 1, 4, label=PRODUCT) # create a Span for the new entity
    nlp_obj.ents = list(nlp_obj.ents) + [igp]
    '''




    # STOPPED HERE
    PRODUCTID = nlp_obj.vocab.strings[u"PRODUCTID"]
    for token in nlp_obj:
        i = 0
        for id in product_ids:
            if token.text == id:
                start = token.i
                end = token.nbor().i
                print('token: {}, token start: {}, token end: {}'.format(token.text, start, end))

                pid = Span(nlp_obj, start, end, label=PRODUCTID)
                nlp_obj.ents = list(nlp_obj.ents) + [pid]

                i += 1

    #print('found{} product ids.\n'.format(found))

    print('\nAfter')
    ents = [(e.text, e.start_char, e.end_char, e.label_) for e in nlp_obj.ents]

    for e in nlp_obj.ents:
        print(e.text, e.label_)

    print('\n\n')
    '''
    for token in nlp_obj:
        print(token.text, token.tag_)
    '''


if __name__ == '__main__' : main()
