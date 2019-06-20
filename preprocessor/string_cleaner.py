# -*- coding: utf-8 -*-
"""
Created on Thur Jun 13 14:49:44 2019
@author: Stacy

scripts to perform cleaning operations on a doc and return it to caller

preprocessor/
    string_cleaner.py
    # imports: [ unicodedata2, re ]
        # helper functions
            # def lemmatizer(d)
            def remove_accents(d)
            def remove_special_chars(d)
            def remove_whitespace(d)
            def normalizer(d)
            def apply_custom_rules(d)
        # controller function
            def string_cleaner(d)

"""
# IMPORT LIBS  =====================================
import unicodedata2
import re

# IMPORT PATHS  ====================================

# IMPORT FUNCTIONS  ================================
import loader

# GLOBALS  =========================================
# define special characters to be removed from doc
# rem keep '/' for cases such as 1/2 kg, etc
# rem keep ':' for skus that need it
# rem keep ',' for numbers that need it
# rem keep '.' for numbers that need it
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(',
                ')', '{', '}', '[', ']', '|', '\\', ';', '\"',
                '\'', '<', '>', '?', '£']

# HELPER FUNCTIONS  =================================
def lemmatizer(d): pass

def remove_accents(d):
    # rem unicode is default on python3
    try:
        d = unicode(d, 'utf-8')
    except (TypeError, NameError):
        pass

    d = unicodedata2.normalize('NFC', d)
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

def apply_custom_rules(d):
    return d

# CONTROLLER FUNCTION  =============================
def clean_doc(d):
    # d = lemmatizer(d)
    d = remove_accents(d)
    d = remove_special_chars(d)
    d = remove_whitespace(d)
    d = normalizer(d)
    d = apply_custom_rules(d)

    return d
    # end function //
