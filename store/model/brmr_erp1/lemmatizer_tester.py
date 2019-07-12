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

# MAIN  --------------------------------
def main():
    # example
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    lemmas = lemmatizer(u'fuses', u'NOUN')
    print(lemmas)

    # create nlp doc
    nlp = spacy.load('en_core_web_sm')
    print(nlp.pipe_names)
    doc = nlp(u'50123 is a I need 50 FAG ball bearings and a pump with a SKU of 523421 and a MPN of 1234-12')

    s = ''
    for tok in doc:
        if tok.is_stop == False:
            if tok.text == lemmatizer(tok.text, tok.pos_):
                print(lemmatizer(tok.text, tok.pos_), tok.pos_, tok.tag_, end='')
    print('\n{}'.format(doc))

    for ent in doc.ents:
        print(ent.text, ent.label_)


    # end program
    print('\nDone.')


if __name__ == '__main__' : main()
