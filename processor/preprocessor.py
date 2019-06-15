# -*- coding: utf-8 -*-
"""
Created on Thur Jun 13 14:49:44 2019
@author: Stacy

processor/
    preprocessor.py
    # imports: [jellyfish, spacy, re, unicodedata2]
        def string_cleaner(d)
        def remove_accents(d)
        def remove_special_chars(d)
        def remove_whitespace(d)
        def remove_stop_words(d)
        def normalizer(d)
        def lemmatizer(d)
        def porterStemmer(d)
        def remove_stop_words(d)

"""

# IMPORTS  =========================================
import re # good
import jellyfish
import unicodedata2
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en.examples import sentences

# GLOBALS  =========================================
# define special characters to be removed by the string cleaner
# rem periods are important, please do not remove them
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                '{', '}', '[', ']', '|', '\\', ':', ';', '\"', '\'',
                '<', ',', '>', '?', '/']

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

# perform look-up based lemmatization
# rem to provide a lookup lemmatizer for your language, import the lookup
# table and add it to the Language class as lemma_lookup:
def lemmatizer(d):
    pass

def normalizer(d):
    d = d.lower()
    return d

# Reduce the string token to its stem and return root word
def porterStemmer(s):
    # print('Porter Stemmer...')
    return jellyfish.porter_stem(s)

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

# remove stop words from doc object
#   stop words are most common filter words
#   rem matching tokens will return True for is_stop
#   you need to create nlp object before working with stop words
#   because the doc needs to be tokenized
def remove_stop_words(d):

    # TEST
    #print(d.text)
    for token in nlp_obj:
        print(token.text)
    '''
    for word in d:
        if word.is_stop == True:
            print(word)
    '''
    return d
