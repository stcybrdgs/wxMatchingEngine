# -*- coding: utf-8 -*-
"""
Created on Thur Jun 13 14:49:44 2019
@author: Stacy


processor/

"""

# IMPORTS  =========================================
import re
import jellyfish
import spacy
from spacy.lang.en.examples import sentences


# GLOBALS  =========================================
STOP_WORDS = set("""
a about above across after afterwards again against all almost alone along
already also although always am among amongst amount an and another any anyhow
anyone anything anyway anywhere are around as at back be became because
become becomes becoming been before beforehand behind being below beside
besides between beyond both bottom but by
""".split())

# define special characters to be removed by the string cleaner
# rem periods are important, please do not remove them
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                '{', '}', '[', ']', '|', '\\', ':', ';', '\"', '\'',
                '<', ',', '>', '?', '/']


# FUNCTIONS  =======================================
def string_cleaner(d):
    print('Running Preprocessor...')
    d = remove_special_chars(d)
    d = remove_stop_words(d)
    d = remove_whitespace(d)
    #clean_doc = lemmatizer(clean_doc)
    d = normalizer(d)
    # normalize text
    # stemmer
    return d


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
# rem stop words are most common words that are useful to filter out
# rem stop words are separated by spaces and newlines and added as a multiline string.
# rem matching tokens will return True for is_stop
def remove_stop_words(d):
    return d
