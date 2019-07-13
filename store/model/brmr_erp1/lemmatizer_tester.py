#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
'''
Thursday, July 11, 2019
Stacy Bridges

Lemmatizer Tester

'''
# IMPORTS  -----------------------------
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lang.en.stop_words import STOP_WORDS
import sys
import os

# IMPORT PATHS  ====================================
sys.path.append('../../../preprocessor/')

# IMPORT FUNCTIONS  ================================
import string_cleaner

# GLOBALS  =========================================
nlp = spacy.load('en_core_web_sm')

# MAIN  ============================================
def main():
    # example
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    lemmas = lemmatizer(u'fuses', u'NOUN')
    #print(lemmas)

    # create nlp doc
    print(nlp.pipe_names)
    doc = nlp(u'50123, 50 FAG ball bearings with a SKU of 523421 and a MPN of 1234:1')

    # stop words
    str_doc = ''
    for tok in doc:
        if tok.is_stop == False:
            str_doc = str_doc + tok.text + ' '

    print('stop_words: ')
    print('\n{}'.format(doc))
    print('{}'.format(str_doc))

    doc2 = nlp(str_doc)

    # lemmatizer
    str_doc2 = ''
    print('\nlemmatized toks:')
    for tok in doc2:
        # rem a lemmatized string is returned as a list
        # so it must be indexed to be 'unpacked' for string comparison
        if tok.text != lemmatizer(tok.text, tok.pos_)[0]:  # and tok.pos_ == 'NOUN':
            print(tok.text, lemmatizer(tok.text, tok.pos_), tok.pos_, tok.tag_, '\n')
            str_doc2 = str_doc2 + str(lemmatizer(tok.text, tok.pos_)[0]) + ' '
        else:
            str_doc2 = str_doc2 + tok.text + ' '

    print('\n{}'.format(doc2))
    print('{}'.format(str_doc2))

    print('\ntoks:')
    for tok in doc:
        print(tok.text, tok.pos_)
    print('\nents:')
    for ent in doc.ents:
        for tok in ent:
            print(tok.text)
            #if tok.text != lemmatizer(tok.text, tok.pos_)[0]:
            #    print(ent.label_, ent.text)
    #for ent in doc.ents:
    #    print(ent.text, ent.label_)

    # end program
    print('\nDone.')


if __name__ == '__main__' : main()
