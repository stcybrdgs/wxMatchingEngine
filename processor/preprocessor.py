# -*- coding: utf-8 -*-
"""
Created on Thur Jun 13 14:49:44 2019
@author: Stacy


processor/

"""

# IMPORTS  =========================================
import jellyfish
import spacy
from spacy.lang.en.examples import sentences


# GLOBALS  =========================================
STOP_WORDS = set("""
a about above across after afterwards again against all almost alone along
already also although always am among amongst amount an and another any anyhow
anyone anything anyway anywhere are around as at

back be became because become becomes becoming been before beforehand behind
being below beside besides between beyond both bottom but by
""".split())

special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                '{', '}', '[', ']', '|', '\\', ':', ';', '\"', '\'',
                '<', ',', '>', '.', '?', '/']

# FUNCTIONS  =======================================
def string_cleaner(d):
    print('Running Preprocessor...')
    # remove special characters
    clean_doc = remove_special_chars(d)

    # nltk stopwords

    # lemmatizer / stemmer

# perform look-up based lemmatization
# rem to provide a lookup lemmatizer for your language, import the lookup
# table and add it to the Language class as lemma_lookup:
def lemmatizer(d):
    pass

'''
Reduce the string s to its stem using the common Porter stemmer.
Stemming is the process of reducing a word to its root form, for example ‘stemmed’ to ‘stem’.
Martin Porter’s algorithm is a common algorithm used for stemming that works for many purposes.
'''
# remove suffixes and return root word
def porterStemmer(s):
    # print('Porter Stemmer...')
    return jellyfish.porter_stem(s)



def remove_special_chars(d):
    print('Removing special characters... ') # test
    print('Before: ' + d)
    for char in special_chars:
        if d.find(char) >= 0:
            print(char)
            d = d.replace(char, ' ')
    print('After: ' + d)
    return d

# remove stop words from doc object
# rem stop words are most common words that are useful to filter out
# rem stop words are separated by spaces and newlines and added as a multiline string.
# rem matching tokens will return True for is_stop
def stop_words(d):
    pass
