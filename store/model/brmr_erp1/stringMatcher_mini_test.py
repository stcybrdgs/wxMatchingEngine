# -*- coding: utf-8 -*-
'''
Created July 5 2019
Stacy Bridges

The rule-matching engine (the Matcher) operates over tokens in a way that's
similar to regular expressions. The rules can refer to token annotations
(e.g. the token text or tag_, and flags (e.g. IS_PUNCT). The rule matcher also
lets you pass in a custom callback to act on matches – for example, to merge
entities and apply custom labels. You can also associate patterns with entity IDs,
to allow some basic entity linking or disambiguation. To match large terminology
lists, you can use the PhraseMatcher, which accepts Doc objects as match patterns.


'''
# IMPORTS  =====================================
import os
import sys
import spacy
from spacy.matcher import Matcher
from spacy.pipeline import Tagger
import csv
from spacy.pipeline import EntityRuler
from pathlib import Path
import jellyfish
#from .stop_words import STOP_WORDS
#from spacy.lang.en import English

# PATHS  =======================================
sys.path.append('../../../preprocessor/')

# IMPORT PY FILES  =============================
import string_cleaner
import loader

# GLOBALS  =====================================
global row_heads
row_heads =[]

# FUNCTIONS  ===================================
def sentence_segmenter(doc):
    global row_heads

    # get the list of row heads
    row_heads = loader.get_row_heads()
    j = 0

    # normalize row heads so that they can be compared to text in nlp obj
    for rh in row_heads:
        row_heads[j] = string_cleaner.normalizer(rh)
        j += 1

    # set each row head as a sentence start
    j = 0
    for rh in row_heads:
        for token in doc:
            if token.text == rh[:2]:
                doc[token.i].is_sent_start = True
        j += 1

    return doc
    # end function //

# MAIN  ==========================================
def main():
    global row_heads

    nlp = spacy.load('model')  # load the pre-trained model with entity ruler

    # add pipe components
    nlp.add_pipe(sentence_segmenter, before='entity_ruler')

    #tagger = nlp.create_pipe("tagger")
    #tagger = Tagger(nlp.vocab)
    #nlp.add_pipe(tagger, after='sentence_segmenter')

    # initialize Matcher with a vocab
    # rem Matcher must share vocab with documents
    #     it operates upon
    matcher = Matcher(nlp.vocab)

    # show pipeline components:
    print(nlp.pipe_names)

    # call matcher.add with no callback and one custom pattern
    # (if you use a callback, it is invoked on a successful match)
    # rem each dictionary represents one token
    pattern_1 = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
    pattern_2 = [{"LOWER": "hello"}, {"LOWER": "world"}]

    matcher.add("HelloWorld", None, pattern_1, pattern_2)

    doc = nlp(u"Hello, world! Hello! Hello world! Hello, there, world!")
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)

    tender = nlp(string_cleaner.clean_doc(loader.load_doc('matcher/mini_tender.csv')))
    # show row_heads
    print('Tender row_heads: ', row_heads)

    erp = nlp(string_cleaner.clean_doc(loader.load_doc('matcher/mini_erp.csv')))
    # show row_heads
    print('ERP row_heads: ', row_heads)

    print('\nERP:  -------------------\\')
    print(erp)

    print('\nTENDER:  -------------------\\')
    print(tender)

    print('\nERP SENTS: -------------------')
    for sent in erp.sents:
        print(sent.text, end='')

    print('\nTENDER SENTS: -------------------')
    for sent in tender.sents:
        print(sent.text, end='')

    print('\nTENDER ENTS: -------------------')
    for sent in tender.sents:
        for ent in sent.ents:
            print(ent.text, ent.label_)

    print('\nTENDER TOKENS: -------------------')
    #tokens = [token.text for token in doc if not token.is_stop]
    for sent in tender.sents:
        for token in sent:
            if not token.is_stop:
                print(token.text, token.ent_type_)

    # by default, the matcher only returns matches and nothing else.
    # if you want it to merge entities, assign labels, or something else,
    # then you can define such actions for each pattern by passing in a
    # callback function as the on_match argument on add(), ie:
    # matcher.add("StringID", myCallBack, pattern)

    # end program
    print('\n\nDone.')

if __name__ == '__main__' : main()
