#!/usr/bin/env python
# coding: utf8
"""
Wed, Nov 6, 2019
Stacy Bridges

This code transforms a column of Brands into patterns that can be used by the NERS
EntityRuler to map Brands to the Brand entity label within a statistical model.
This code uses an NLP object tokenizer to identify break-points between tokens,
and then it wraps the individual tokens in JSONL syntax.

- input: .xlsx or .csv
- output: .jsonl

"""
# LIBRARY IMPORTS  =============================================================
import os, sys, csv  # utilities
from pathlib import Path
import spacy
from spacy import displacy
from spacy.pipeline import EntityRuler, Tagger
from spacy.language import Language
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import unicodedata  # use to normalize international characters
import pandas as pd
from pandas import ExcelWriter
import numpy as np

# HELPER FUNCTIONS  ============================================================
def get_folder_path():
    # return path of current folder
    return os.path.dirname(os.path.abspath(__file__))
    # end function //

def sentence_segmenter(doc):
    # set start pos for each record (sentence) in nlp doc and return doc to caller
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
            # rem add 'wrwx' marker to each record to assist the sentence segmenter
            doc = doc + 'wrwx ' + ('|'.join(row) + '\n')
            i += 1
    return doc
    # end function //

def import_xlsx(d):
    doc = ''
    brnd_data = pd.read_excel(d, 'Sheet1')
    brnd = brnd_data['BRAND']
    # prime the doc object with a header row to keep it aligned with the format
    # used for csv import (ie, the header is not included in the pandas col array)
    doc = doc + 'wrwx' + 'brnd' + '\n'
    for brnd in brnd:
        brnd = str(brnd)  # eliminate any float objects
        brnd = unicodedata.normalize('NFKD', brnd).encode('ASCII', 'ignore')  # convert int'l chars
        brnd = brnd.decode('utf-8')  # convert bytes to strings
        # rem add 'wrwx' marker to each record to assist the sentence segmenter
        doc = doc + 'wrwx ' + brnd + '\n'
    return doc
    # end function //

# MAIN  ========================================================================
def main(file_name = 'db_brnd_gold_test.csv'):  # default arg is a test file

    # get file and file extension
    f_name, file_ext = os.path.splitext(file_name)

    # define i/o
    folder_path = get_folder_path()  # get path of current folder
    brnd_file = folder_path + '\\' + file_name
    ofile = folder_path + '\\' + 'ners_' + file_name[0:len(file_name)-len(file_ext)] + '_patterns.jsonl'

    # load spacy statistical model
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])  # load blank english model
    nlp.add_pipe(sentence_segmenter, after='tagger')  # add custom segmenter to nlp pipeline

    # import brnd file
    if file_ext == '.csv':
        brnd_file = import_csv(brnd_file)  # import as csv if csv
    elif file_ext == '.xlsx':
        brnd_file = import_xlsx(brnd_file)  # import as xlsx if xlsx
    brnd_file = brnd_file.lower()  # convert tender data to lowercase
    doc = nlp(brnd_file)  # turn brnd data into nlp object

    patterns = []
    i = 0
    for sent in doc.sents:
        tokens = []
        pattern = ''

        # put tokens from each sentence into the tokens array
        if i > 0:  # skip the header
            for tok in sent:
                if tok.text.isspace():#tok.pos_ == 'SPACE':
                    tokens.append(' ')
                elif tok.text != 'wrwx':
                    tokens.append(tok.text)  # put each token in an array that can call .len()

            # remove trailing white space from the tokens array
            j = 0
            for token in tokens:
                j += 1
                if len(tokens) == j and token == ' ':
                    tokens.pop(j-1)

            # use tokens array to build jsonl patterns for NERS
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
                            token_str = token_str + '\\\\'
                        elif char == '"':
                            token_str = token_str + '\\\"'
                        else:
                            token_str = token_str + char
                    token = token_str
                # build the patterns
                if j == 1:
                    pattern = pattern + '{"label":"BRND", "pattern":['  # pattern prefix
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
    brnd_count = 0
    with open(ofile, 'w') as of:
        for p in patterns:
            print(p)
            of.write(p)
            of.write('\n')
            brnd_count += 1

    # provide console report to user and end the program
    print('\n')
    print('Done.')
    print('JSONL file created.')
    print('{} brnd patterns written to:'.format(brnd_count))
    print('{}'.format(ofile))

if __name__ == '__main__' : main()
