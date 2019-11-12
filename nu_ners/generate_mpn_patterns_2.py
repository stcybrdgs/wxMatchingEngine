#!/usr/bin/env python
# coding: utf8
"""
Mon, Nov 4, 2019
Stacy Bridges

This code transforms a column of MPNs into patterns that can be used by the NERS
EntityRuler to map MPN codes to the MPN entity label within a statistical model.
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
            row = str(row)  # clear float inputs
            row = unicodedata.normalize('NFKD', row).encode('ASCII', 'ignore')  # convert int'l chars
            row = row.decode('utf-8') # convert bytes to strings
            # rem add 'wrwx' marker to each record to assist the sentence segmenter
            doc = doc + 'wrwx ' + ('|'.join(row) + '\n')
            i += 1
    return doc
    # end function //

def import_xlsx(d):
    doc = ''
    mpns_data = pd.read_excel(d, 'Sheet1')
    mpns = mpns_data['MPN']
    # prime the doc object with a header row to keep it aligned with the format
    # used for csv import (ie, the header is not included in the pandas col array)
    doc = doc + 'wrwx' + 'mpn' + '\n'
    for mpn in mpns:
        mpn = str(mpn)  # eliminate any float objects
        mpn = unicodedata.normalize('NFKD', mpn).encode('ASCII', 'ignore')  # convert int'l chars
        mpn = mpn.decode('utf-8')  # convert bytes to strings
        # rem add 'wrwx' marker to each record to assist the sentence segmenter
        doc = doc + 'wrwx ' + mpn + '\n'
    return doc
    # end function //

# MAIN  ========================================================================
def main(file_name = 'db_mpn_gold_test.csv'):  # default arg is a test file

    # get file and file extension
    f_name, file_ext = os.path.splitext(file_name)

    # define i/o
    folder_path = get_folder_path()  # get path of current folder
    mpn_file = folder_path + '\\' + file_name
    ofile = folder_path + '\\' + 'ners_' + file_name[0:len(file_name)-len(file_ext)] + '_patterns.jsonl'

    # load spacy statistical model
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])  # load blank english model
    nlp.add_pipe(sentence_segmenter, after='tagger')  # add custom segmenter to nlp pipeline

    # import mpn file
    if file_ext == '.csv':
        mpn_file = import_csv(mpn_file)  # import as csv if csv
    elif file_ext == '.xlsx':
        mpn_file = import_xlsx(mpn_file)  # import as xlsx if xlsx
    mpn_file = mpn_file.lower()  # convert tender data to lowercase
    doc = nlp(mpn_file)  # turn mpn data into nlp object

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
    mpn_count = 0
    with open(ofile, 'w') as of:
        for p in patterns:
            print(p)
            of.write(p)
            of.write('\n')
            mpn_count += 1

    # provide console report to user and end the program
    print('\n')
    print('Done.')
    print('JSONL file created.')
    print('{} mpn patterns written to:'.format(mpn_count))
    print('{}'.format(ofile))

if __name__ == '__main__' : main()
