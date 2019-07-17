#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
'''
Thursday, July 11, 2019
Stacy Bridges

Matcher Tester

'''
# IMPORTS  -----------------------------
import spacy
import pickle

'''
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lang.en.stop_words import STOP_WORDS
'''

# FUNCTIONS  ===========================
def open_pickle(f):
    pickle_off = open(f,"rb")
    return pickle.load(pickle_off)
    # print('In open_pickle(): ', emp)

# MAIN  --------------------------------
def main():
    # get tender from pickle
    # rem   in final tool the tender would have been
    #       processed by the nlp obj processor and pickled
    # rem   the unpickled tender is already an nlp obj based on the
    #       target model
    nlp_tender = open_pickle('tender.pickle')

    print('\nTender Sentences:')
    for sent in nlp_tender.sents:
        print(sent.text, end='')

    # end program
    print('\nDone.')


if __name__ == '__main__' : main()
