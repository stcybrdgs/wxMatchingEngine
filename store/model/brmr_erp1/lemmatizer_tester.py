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
    #print(lemmas)

    # create nlp doc
    nlp = spacy.load('en_core_web_sm')
    print(nlp.pipe_names)
    doc = nlp(u'50123 is a I need 50 FAG ball bearings and a pump with a SKU of 523421 and a MPN of 1234-12')

    print('\ntoks:')
    s =''
    for tok in doc:
        if tok.is_stop == False:
            # rem a lemmatized string is returned as a list
            # so it must be indexed to be 'unpacked' for string comparison
            if tok.text != lemmatizer(tok.text, tok.pos_)[0] and tok.pos_ == 'NOUN':
                print(tok.text, lemmatizer(tok.text, tok.pos_), tok.pos_, tok.tag_, '\n')
                s = s + str(lemmatizer(tok.text, tok.pos_)[0]) + ' '

    print('\n{}'.format(doc))

    print('\nents:')
    for ent in doc.ents:
        for tok in ent:
            print(tok.text)
            #if tok.text != lemmatizer(tok.text, tok.pos_)[0]:
            #    print(ent.label_, ent.text)
    #for ent in doc.ents:
    #    print(ent.text, ent.label_)

    print('s: {}'. format(s))

    # end program
    print('\nDone.')


if __name__ == '__main__' : main()
