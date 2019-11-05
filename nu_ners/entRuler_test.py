#!/usr/bin/env python
# coding: utf8
"""
Mon, Nov 4, 2019
Stacy Bridges

This simplified code transforms an input set of mpns into mpn patterns
that can be used for string matching by the NERS EntityRuler.

This version uses an nlp object tokenizer to determine the pattern
break points instead of the more complicated rules from previous versions.

"""

# IMPORTS  =====================================
import os, sys, csv, json
import spacy
from spacy import displacy
from spacy.pipeline import EntityRuler
from spacy.pipeline import Tagger
from spacy.language import Language
from pathlib import Path
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lang.en.stop_words import STOP_WORDS
import pandas as pd
from pandas import ExcelWriter
import numpy as np

# FUNCTIONS  ===================================
def sentence_segmenter(doc):
    for token in doc:
        if token.text == 'wrwx':
            doc[token.i].is_sent_start = True
    return doc
    # end function //

def import_csv(d):
    doc = ''
    with open(d) as data:
        csv_reader = csv.reader(data, delimiter='|')
        i = 0
        for row in csv_reader:
            # add top anchor to keep displacy from collapsing
            doc = doc + 'wrwx ' + ('|'.join(row) + '\n')
            i += 1
    # add bottom anchor to keep displacy from collapsing
    return doc
    # end function //

# MAIN  ===========================================
def main():
    # define i/o
    #patterns_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_db_mpn_delme_test_patterns.jsonl'
    mpn_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\db_mpn_delme_test.csv'
    ofile = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_db_mpn_delme_test_patterns.jsonl'

    # load model
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])  # load blank english model
    nlp.add_pipe(sentence_segmenter, after='tagger')  # add custom segmenter to nlp pipeline
    tender = import_csv(mpn_file)  # import tender data
    tender = tender.lower()  # convert tender data to lowercase
    doc = nlp(tender)  # turn tender data into nlp object

    patterns = []
    i = 0
    for sent in doc.sents:
        tokens = []
        pattern = ''
        if i > 0:  # skip the header
            for tok in sent:
                if tok.text.isspace():#tok.pos_ == 'SPACE':
                    tokens.append(' ')
                elif tok.text != 'wrwx':
                    tokens.append(tok.text)  # put each token in an array that can call .len()

            # go thru tokens in the sentence and use them to build the jsonl patterns
            j = 0
            for token in tokens:
                # if the last list index is trailing whitespace, pop it off the list
                j += 1
                if len(tokens) == j and token == ' ':
                    tokens.pop(j-1)
            j = 0
            pattern = ''
            for token in tokens:
                j += 1
                # if the character \ or " exist in the token,
                # then you need to add escape characters to the token
                if token.find('\\') >= 0 or token.find('"') >= 0:
                    token_str = ''
                    for char in token:
                        if char == '\\':
                            #print('here: \\')
                            token_str = token_str + '\\\\'
                        elif char == '"':
                            #print('here: \"')
                            token_str = token_str + '\\\"'
                        else:
                            token_str = token_str + char
                    token = token_str
                # build the patterns
                if j == 1:
                    pattern = pattern + '{"label":"MPN", "pattern":['  # pattern prefix
                if len(tokens) == j:
                    pattern = pattern + '{"lower":"' + token + '"}]}'  # outer pattern (suffix)
                else:
                    pattern = pattern + '{"lower":"' + token + '"},'  # inner pattern
            patterns.append(pattern)  # store the jsonl pattern for this sentence
        tokens.clear()
        i += 1

    # insert starting and ending anchors to prevent the displacy visualizer from collapsing
    start_anchor = '{"label":"WRWXSTART", "pattern":[{"lower":"wrwxstart"}]}'
    end_anchor = '{"label":"WRWXEND", "pattern":[{"lower":"wrwxend"}]}'
    patterns.append(start_anchor)
    patterns.append(end_anchor)

    # write patterns to jsonl pattern file
    with open(ofile, 'w') as of:
        for p in patterns:
            print(p)
            of.write(p)
            of.write('\n')

    # end program
    print('Done.')

if __name__ == '__main__' : main()
