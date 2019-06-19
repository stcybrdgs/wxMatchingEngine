# -*- coding: utf-8 -*-
"""
Created on Thur Jun 13 14:49:44 2019
@author: Stacy

scripts to perform cleaning operations on a doc and return it to caller

preprocessor/
    preprocessor.py
    # imports: [jellyfish, spacy, re, unicodedata2]
        def string_cleaner(d)
        def remove_accents(d)
        def remove_special_chars(d)
        def remove_whitespace(d)
        def normalizer(d)
        # def lemmatizer(d)
"""

# IMPORT LIBS  =====================================
import re
import jellyfish  # for porter stemmer
import unicodedata2
import spacy
import os

# IMPORT PATHS  ====================================

# IMPORT FUNCTIONS  ================================
import loader

# GLOBALS  =========================================
# define special characters to be removed by the string cleaner
# rem periods are important, please do not remove them
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                '{', '}', '[', ']', '|', '\\', ';', '\"', '\'',
                '<', '>', '?']
                # keep '/' for cases such as 1/2 kg, etc
                # keep ':' for skus that need it
                # keep ',' for numbers that need it

# HELPER FUNCTIONS  =================================
def remove_accents(d):
    # rem unicode is default on python3
    try:
        d = unicode(d, 'utf-8')
    except (TypeError, NameError):
        pass

    d = unicodedata2.normalize('NFD', d)
    d = d.encode('ascii', 'ignore')
    d = d.decode("utf-8")
    return str(d)
    # end function //

def remove_special_chars(d):
    for char in special_chars:
        if d.find(char) >= 0:
            d = d.replace(char, ' ')
    return d
    # end function //

def remove_whitespace(d):
    d = d.strip()  # remove leading and trailing whitespace
    d = re.sub(' +', ' ', d)  # remove duplicative whitespace
    return d
    # end function //

# change all strings to lowercase
def normalizer(d):
    d = d.lower()
    return d
    # end function //

# perform look-up based lemmatization if needed
# rem to provide a lookup lemmatizer for detected language, import the lookup
# table and add it to the Language class as lemma_lookup:
def lemmatizer(d):
    pass
    # end function //

# CONTROLLER FUNCTION  =============================
def string_cleaner(d):
    d = remove_accents(d)
    d = remove_special_chars(d)
    d = remove_whitespace(d)
    d = normalizer(d)
    # d = lemmatizer(d)

    return d
    # end function //
