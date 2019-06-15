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
    # remove special characters
    clean_doc = remove_special_chars(d)
    clean_doc = remove_whitespace(clean_doc)
    return clean_doc

    # nltk stopwords

    # lemmatizer / stemmer

# perform look-up based lemmatization
# rem to provide a lookup lemmatizer for your language, import the lookup
# table and add it to the Language class as lemma_lookup:
def lemmatizer(d):
    pass


# Reduce the string token to its stem and return root word
def porterStemmer(s):
    # print('Porter Stemmer...')
    return jellyfish.porter_stem(s)

# remove special characters from the doc object
# and return to caller
def remove_special_chars(d):
    for char in special_chars:
        if d.find(char) >= 0:
            print(char)
            d = d.replace(char, ' ')
    return d

'''
list = ['item', 'thing', 'string']
for i in list:
    z = re.match('(g\w+)\W(g\w+)', i)
    if z: #do something
'''
def remove_whitespace(d):
    d = re.sub(' +', ' ', d)
    return d

# remove stop words from doc object
# rem stop words are most common words that are useful to filter out
# rem stop words are separated by spaces and newlines and added as a multiline string.
# rem matching tokens will return True for is_stop
def stop_words(d):
    pass
