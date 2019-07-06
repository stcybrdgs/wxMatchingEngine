# !/usr/bin/env python
# coding: utf8
# model trainer test
# Compatible with: spaCy v2.0.0+

'''
Friday, July 5, 2019
Stacy Bridges

'''
# LIB IMPORTS =================================
#from __future__ import unicode_literals, print_function
#import plac
#import random
#from pathlib import Path
import spacy
#from spacy.util import minibatch, compounding
#from spacy.tokens import Token
#import sys
#import os

def main():
    # load trained model
    #from spacy.language import Language
    from spacy.language import English
    #nlp = spacy.load("model/")
    nlp = English().from_disk("model/")

    doc = nlp(u'FAG DEEP GROOVE BALL BEARING 6026-2RSRC3, I need another ball bearing, deep groove, by FAG')

    #for token in doc:
    #    print(token.text, token.ent_type_)
    print([(ent.text, ent.label_) for ent in doc.ents])

    # end program
    print('Done.')

if __name__ == '__main__' : main()
