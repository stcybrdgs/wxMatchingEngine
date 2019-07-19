# -*- coding: utf-8 -*-
'''
Friday Jul 19 2019
Stacy Bridges

looking for mMat ids within product data

'''
# IMPORTS  ---------------------------------------------------------
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import sys
import os
import re

# IMPORT PATHS  ====================================
#sys.path.append('../parameters/')
sys.path.append('../../../preprocessor')

# IMPORT FILES  ====================================
import string_cleaner
#import stop_words

# GLOBALS  ---------------------------------------------------------

# FUNCTIONS  -------------------------------------------------------
def sentence_segmenter(doc):
    for token in doc:
        if token.text == 'root':
            doc[token.i].is_sent_start = True
    return doc
    # end function //

# MAIN  ------------------------------------------------------------
def main():
    # get iesa descriptions from external file
    p_strings = []
    with open('iesa_short_descriptions.txt', 'r') as infile:
        for line in infile:
            p_strings.append(re.sub(r'^\s+$', '', line))

    # get suppliers and iesa stop words from external file and add to iesa_stop_words[]
    iesa_stop_words = []

    with open('suppliers.txt', 'r') as infile:
        for word in infile:
            iesa_stop_words.append(word.lower().strip())

    with open('iesa_stop_words.txt', 'r') as infile:
        for word in infile:
            iesa_stop_words.append(word.lower().strip())

    # program controller  ------------------------------------------------------
    nlp_switch = 'on'
    nlp_features = 'st'
    # s, t, st, nc, m   ->  sents, toks, sents + toks, noun-chunks, mmat

    # --------------------------------------------------------------------------

    # build the string to use for nlp based on iesa short description
    nlpstr = ''
    i = 0
    for item in p_strings:
        nlpstr = nlpstr + 'root ' + p_strings[i] + ' '
        i += 1

    nlpstr = string_cleaner.clean_doc(nlpstr)
    #nlpstr = nlpstr.lower()
    #nlpstr = nlpstr.strip()  # remove leading and trailing whitespace
    #nlpstr = re.sub(' +', ' ', nlpstr)  # remove duplicative whitespace

    spacer = '----------------------'
    #print(spacer)
    #print(nlpstr)

    '''
    STRING TESTING
    '''

    # --------------------------------------------------------------------------
    def nlp_stuff(nlpstr, feature):
        # make nlp object
        nlp = spacy.load('en_core_web_sm', disable=['parser'])
        nlp.add_pipe(sentence_segmenter, before='ner')
        merge_nchunks = nlp.create_pipe('merge_noun_chunks')
        nlp.add_pipe(merge_nchunks)

        # add iesa stop words
        for word in iesa_stop_words:
            nlp.vocab[word].is_stop = True

        # create nlp object
        d = nlp(nlpstr)
        print(nlp.pipe_names)  # test print

        # print sentences to console
        if feature == 's' or feature == 'st':
            for sent in d.sents:
                print(sent)

        # print tokens to console
        if feature == 't' or feature == 'st':
            print(spacer)
            for sent in d.sents:
                for tok in sent:
                    if tok.is_stop == False:
                        print(tok.text, tok.pos_, tok.tag_)
                print(spacer)

        # print noun chunks to console
        if feature == 'nc':
            print(spacer)
            for nc in d.noun_chunks:
                print(nc.text)
            print(spacer)

        # print mMat to console
        if feature == 'm':
            print(spacer)
            for sent in d.sents:
                for tok in sent:
                    if tok.is_stop == False and tok.text != 'root' and tok.pos_ in ['NOUN', 'NUM', 'ADJ']:
                        print(tok.text, tok.pos_, tok.tag_)
                print(spacer)

    # --------------------------------------------------------------------------

    if nlp_switch == 'on':
        nlp_stuff(nlpstr, nlp_features)

    # end program
    print('\nDone.')

if __name__ == '__main__': main()
