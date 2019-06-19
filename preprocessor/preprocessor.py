# -*- coding: utf-8 -*-
"""
Created on Thur Jun 13 14:49:44 2019
@author: Stacy

preprocessor/
    preprocessor.py
    # imports: [jellyfish, spacy, re, unicodedata2]
        def string_cleaner(d)
        def remove_accents(d)
        def remove_special_chars(d)
        def remove_whitespace(d)
        def normalizer(d)
        # def lemmatizer(d)
        def porterStemmer(d)

"""

# IMPORT  LIBS  ========================
import re
import jellyfish  # for porter stemmer
import unicodedata2
import spacy
import os

# IMPORT FUNCTIONS  =====================
import loader

# GLOBALS  =========================================
# define special characters to be removed by the string cleaner
# rem periods are important, please do not remove them
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                '{', '}', '[', ']', '|', '\\', ';', '\"', '\'',
                '<', '>', '?']
                # leave in '/' for cases such as 1/2 kg, etc
                # leave in ':' for skus that use it
                # leave in ',' for EU numerical data that uses it

# FUNCTIONS  =======================================
def string_cleaner(d):
    d = remove_accents(d)
    d = remove_special_chars(d)
    d = remove_whitespace(d)
    d = normalizer(d)
    # d = lemmatizer(d)
    # porterStemmer
    return d

# remove accents from a doc / string
# receive doc obj as d and return processed obj
def remove_accents(d):
    try:
        d = unicode(d, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python3
        pass
    d = unicodedata2.normalize('NFD', d)
    d = d.encode('ascii', 'ignore')
    d = d.decode("utf-8")
    return str(d)

# remove special characters from the doc object
# and return to caller
def remove_special_chars(d):
    for char in special_chars:
        if d.find(char) >= 0:
            d = d.replace(char, ' ')
    return d

# remove leadin, trailing, and duplicative whitespace
def remove_whitespace(d):
    d = d.strip()  # remove leading and trailing whitespace
    d = re.sub(' +', ' ', d)  # remove duplicative whitespace
    return d

# change all strings to lowercase
def normalizer(d):
    d = d.lower()
    return d

# perform look-up based lemmatization
# rem to provide a lookup lemmatizer for your language, import the lookup
# table and add it to the Language class as lemma_lookup:
def lemmatizer(d):
    pass

# Reduce the string token to its stem and return root word
def porterStemmer(s):
    # print('Porter Stemmer...')
    return jellyfish.porter_stem(s)
