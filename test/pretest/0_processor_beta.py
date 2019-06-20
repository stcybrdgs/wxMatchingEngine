# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19
@author: Stacy Bridges

"""

# IMPORT LIBS  ======================================
import spacy
from spacy.tokens import Span
from spacy.tokens import Token
# from spacy.strings import StringStore
import csv
import sys
import os

# PATHS ================================
sys.path.append('../../preprocessor/')

# IMPORT FILES  ========================
import string_cleaner

# GLOBALS  ==============================
global product_ids
product_ids = []

# CUSTOM PIPES  =========================
def stop_wordser(): pass
def colname_tagger(): pass
def commonkey_tagger(arg): pass
def sentence_segmenter(): pass

# MAIN  =================================
def main():
    # get english language model
    nlp = spacy.load('en_core_web_sm') #, disable=['parser'])

    # custom pipeline:
    #   tokenizer > tagger
    #   colname_tagger> common_key_tagger > sentence_segmenter >
    #   parser > ner
    # consider adding: entity_ruler, merge_noun_chunks (https://spacy.io/usage/processing-pipelines/)
    nlp.add_pipe(sentence_segmenter, name="sentence_segmenter", before="parser")
    nlp.add_pipe(commonkey_tagger, name="commonkey_tagger", before="sentence_segmenter")
    nlp.add_pipe(colname_tagger, name="colname_tagger", before="commonkey_tagger")
    nlp.add_pipe(stop_wordser, name="stop_wordser", before="colname_tagger")

    print(nlp.pipe_names)  # test print



    print('Done')

if __name__ == '__main__' : main()
