# -*- coding: utf-8 -*-
'''
Created on Tue Jun 18 2019
@author: Stacy Bridges
'''
import spacy
from spacy.tokens import Token

def main():
    nlp = spacy.load('en_core_web_sm')

    fruit_getter = lambda token: token.text in (u"apple", u"pear", u"banana")
    pid_getter = lambda token: token.text in (u'123a123', u'1234', u'123123123')
    Token.set_extension("is_fruit", getter=fruit_getter)
    Token.set_extension("is_pid", getter=pid_getter)
    doc = nlp(u"I have an apple, a pear, and a watermelon")
    doc2 = nlp(u'123a123 SKF-23-Pump Handle Made to last')
    assert doc[3]._.is_fruit
    for token in doc:
        if token._.is_fruit:
            print('found: {}'.format(token.text))
    for token in doc2:
        if token._.is_pid:
            print('{} is a product id'.format(token.text))

    print('Done')

if __name__ == '__main__' : main()
