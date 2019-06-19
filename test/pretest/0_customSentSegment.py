# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18
@author: Stacy Bridges

script to make custom sentence segmenter
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
global product_ids
product_ids = []

# CUSTOM PIPES  =========================
def field_val_tagger():
    global product_ids

    PRODUCTID = nlp_obj_cln.vocab.strings[u"PRODUCTID"]
    pid = ''
    for token in nlp_obj:
        i = 0
        for i in product_ids:
            if token.text == product_ids[i]
                pid = product_ids[i]
                nlp_obj_cln.ents = list(nlp_obj_cln.ents) + pid

def custom_sentencizer(doc):
    pass
    '''
    for i, token in enumerate(doc[:-2]):
        # Define sentence start if pipe + titlecase token
        if token.text == "|" and doc[i+1].is_title:
            doc[i+1].is_sent_start = True
        else:
            # Explicitly set sentence start to False otherwise, to tell
            # the parser to leave those tokens alone
            doc[i+1].is_sent_start = False
    '''

    return doc

def common_key_tagger(doc):
    #print("After tokenization, this doc has {} tokens.".format(len(doc)))
    #print("The part-of-speech tags are:", [token.pos_ for token in doc])
    if len(doc) < 10:
        #print("This is a pretty short document.")
        pass
    return doc

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
    nlp.add_pipe(field_val_tagger, name = "field_val_tagger", last=True)
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
                product_id = row[0]
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


    # observations:
    # if you don't clean the txt_obj, spacy sees all records as one sentence

    # TEST PRINT  -----------------------
    # print('\n\ntxt_obj after cleaning:\n', txt_obj)  # test print

    # create the nlp object:
    print('\n\ntxt_obj:')
    i = 0
    for sent in nlp_obj.sents:
        print(sent.text, '**end**\n\n')
        i += 1

    # TEST print text attributes  -----------------------
    '''
    i = 0
    for sent in nlp_obj.sents:
        print(sent.text, '**end**\n\n')
        i += 1
    #print('\n\n# of sents: ', i)  # test print
    d = ' | '
    # text attributes
    attr = [ 'i','text','lemma_','tag_','ent_type_','ent_iob_',
            'ent_id_','is_alpha','is_digit','is_punct','is_space',
            'like_num']
    for token in nlp_obj:
        print(token.text, token.i, token.tag_, token.pos_)
        print(token.ent_type_, token.ent_iob_, token.ent_id_)
        print(token.is_alpha, token.is_digit, token.is_punct)
        print(token.is_space, token.like_num)
        print('\n\n')
    '''

if __name__ == '__main__' : main()
