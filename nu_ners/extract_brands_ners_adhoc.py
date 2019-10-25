#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
# extract_brands_ners_adhoc.py
"""
Wed, Oct 23, 2019
Stacy Bridges
"""
# EXTRACT BRANDS
# get data file input
# get brand input
# choose which data column to use for extraction
#    - program presents user with menu of options
# get fresh model
#    - use entity ruler and brands input to map brands
#    - chunk as needed
# get data column
#    - turn into nlp
#    - chunk as needed
# extract brands into single column
#    - extract as list of distinct brands
#    - if brands are already in the column, preserve them
# after extracting, run script to identify primary brand

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

# PATHS  =======================================
#sys.path.append('../../../preprocessor')

# IMPORT PY FILES  =============================
import py_string_cleaner

# GLOBALS  =====================================
global row_heads
row_heads = []

# FUNCTIONS  ===================================
def sentence_segmenter(doc):
    for token in doc:
        if token.text == 'wrwx':
            doc[token.i].is_sent_start = True
    return doc
    # end function //

def import_csv(d):
    global row_heads
    doc = ''
    with open(d) as data:
        csv_reader = csv.reader(data, delimiter='|')
        i = 0
        for row in csv_reader:
            # populate row_heads[]
            #if i > 0:  # skip header row
            row_head = row[0]
            row_heads.append(row_head)
            # populate txt obj
            doc = doc + 'wrwx ' + ('|'.join(row) + '\n')
            i += 1
    return doc
    # end function //

# MAIN  ========================================
def main():
    '''
    NERS Demo w/ Sample Data
    '''
    print('\nNERS - extract Brands (ad hoc)')

    # CONFIG  -------------------------------------------------- \\
    # ------------------------------------------------------------ \\

    # brnd, mpn, spplr
    model = 'pre'   # pre -> use non-trained model / post -> use trained model
    brnd = 'on'  # on/off
    ruler = 'on'
    cleaner = 'on'
    number_tagger = 'off'

    # rem if stemmer is turned on after model does P2 training, then
    # you will need to use POS tag to detect nouns in products
    # then create new generator patterns for all.json
    # then run entity ruler again
    # stemmer = 'off'

    #outFile = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_brand_patterns.jsonl'
    # declare outputs
    brnd_pandas_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\00_ners_out_brands.xlsx'  # output
    wx_1_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\test_data_cln_org_iesa_PPE_wx_v1.xlsx' # output

    # declare inputs
    brnd_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_brand_patterns.jsonl'  # input
    patterns_file = brnd_file

    tender_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\test_brands_old_input.csv'
    #tender_file = r'C:\Users\stacy\Desktop\NERS Demo\descriptions_nonstock.csv'
    write_type = 'w'

    # ------------------------------------------------------------ //
    # ---------------------------------------------------------- //

    # SETUP PD DATAFRAMES  -----------------------------------------------------
    # read Brands infile into pd dataframe
    # read Tender infile into pd dataframe

    # load model
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) #('en_core_web_sm', disable=['parser'])
    #elif model == 'post':nlp = spacy.load('demo_model')
    nlp.add_pipe(sentence_segmenter, after='tagger')

    # add pipes
    if ruler == 'on':
        # load patterns from external file only if model is not already trained
        nu_ruler = EntityRuler(nlp).from_disk(patterns_file)
        # putting the ruler before ner will override ner decisions in favor of ruler patterns
        nlp.add_pipe(nu_ruler)#, before='ner')
        '''
        # remember to swap precedence between ruler and ner after model training
        if model == 'post':
            # load patterns from external file only if model is not already trained
            if "entity_ruler" not in nlp.pipe_names:
                nu_ruler = EntityRuler(nlp).from_disk(patterns_file)
                # putting the ner before ruler will override favor ner decisions
                nlp.add_pipe(nu_ruler)#, before='ner')
        '''

    # show pipeline components:
    print(nlp.pipe_names)

    # import test tender and clean it up
    tender = import_csv(tender_file)  # import
    if cleaner == 'on':
        tender = py_string_cleaner.clean_doc(tender)  #  clean

    doc = nlp(tender)

    # FIND ENTITIES  -----------------------------------------------------------
    labels = []
    alt_labels = []
    print('\n')
    labels = ['BRND']  # , 'PRODUCT', 'MPN', 'SKU']
    alt_labels = ['Brnd']  # , 'Product', 'MfrPartNo', 'SkuID']
    total_found = []
    total_unique_found = []
    for label in labels:
        tot_num = 0
        unique_num = 0
        unique = []
        for ent in doc.ents:
            # print([ent.text, ent.label_], end='')
            if ent.label_ == label:
                if ent.text not in unique:
                    unique.append(ent.text)
                    unique_num += 1
                tot_num += 1
        print('\nFound {} total, {} unique.\n'.format(tot_num, unique_num))
        total_found.append(tot_num)
        total_unique_found.append(unique_num)

    # pandas output for brnds  ------------------------------------------------
    # This technique allows you to isolate entities on
    # a sentence-by-sentence basis, which will allow
    # for matching entities on a record-by-record basis
    w_Brnds = []
    w_Brnd_Alts = []
    unique = []
    brnd_val = ''
    alts = ''
    #ent_exists = False
    j = 0
    for sent in doc.sents:
        i = 0
        for ent in sent.ents:
            # ignore header record
            if j > 0:
                if ent.label_ == 'BRND':
                    if i == 0:
                        # if it's the first label in the record, save it in brnd
                        brnd_val = ent.text
                        unique.append(ent.text)
                        i += 1
                    else:
                        # if it's not the first label in the sentence, put it in brnd alts
                        # (if it is already in alts, don't put it in)
                        if ent.text not in unique:
                            unique.append(ent.text)
                            if alts == '':
                                alts = ent.text
                            else:
                                alts = alts + ', ' + ent.text
                    #print(ent.label_, ': ', ent.text)

        # store ent results for each record, ignoring the headers
        if j > 0:
            w_Brnds.append(brnd_val.upper())
            w_Brnd_Alts.append(alts.upper())

            # test ---------------
            print('Record: {}'.format(j))
            #print('str ', j, 'w_Brnds: ', w_Brnds)
            #print('str ', j, 'w_Brnd_Alts: ', w_Brnd_Alts)
            # test ---------------

        # reset vars for next record
        unique.clear()
        brnd_val = ''
        alts = ''
        j += 1

        # FOR THE CHUNKER
        # It basically creates a new dataframe object with the new data row
        # at the end of the dataframe. The old dataframe will be unchanged.
        # data = [{'Region':'East','Company':'Shop Rite','Product':'Fruits','Month':'December','Sales': 1265}]
        # df.append(data,ignore_index=True,sort=False)

        # DataFrame.insert(self, loc, column, value, allow_duplicates=False)
        # loc : int # insertion index, must verify0 <= loc <= len(cols)
        # column: string, number, or hashable object -- this is label of inserted col
        # value: int, Series, or array-like
        # allow_duplicates: bool, optional

        # FOR INSERTING BRANDS BACK INTO wx_v1
        # df = pd.DataFrame.insert(0, 'w_Brnds_Test')
        # or
        # df = pd.read_csv("nba.csv")
        # df.get(["Salary", "Team", "Name"])

        df = pd.DataFrame({ 'w_Brnds':w_Brnds,
                            'w_Brnd_Alts':w_Brnd_Alts})

        writer = pd.ExcelWriter(wx_1_file)  #brnd_pandas_file)
        df.to_excel(writer,'NERS_Brnds', index=False)
        writer.save()

    # save the model  --------------------------------------------------------
    # save model with entity pattern updates made by the entity ruler
    output_dir = Path('ners_adhoc_model')
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

    # TEST  -----------------------------
    mpns = []

    # DISPLACY VISUALIZER -----------------------------------------------------
    # get results for html doc
    results = ''
    i = 0
    for item in alt_labels:
        results = results + '{}: {} tot  {} unq\n'.format(item, total_found[i], total_unique_found[i])
        i += 1
    # store nlp object as string in html var
    spacer = '---------------------------------------------------------\n'
    header = 'Named Entities Found in Target File:\n'
    doc = nlp(header + spacer + results + spacer + tender)
    doc.user_data["title"] = "Named Entity Resolution System (NERS)"
    colors = {"BRND": "#FFDDA1"}
    #colors = {"MPN": "#C3FFA1", "BRND": "#FFDDA1", "CMMDTY": "#F3DDA1"}
    options = {"ents": ["MPN", "BRND", "CMMDTY"], "colors": colors}
    # displacy.serve(doc, style="ent", options=options)
    html = displacy.render(doc, style="ent", page=True, options=options)  # use the entity visualizer
    # write the html string to the xampp folder and launch in browser through localhost port
    with open('C:/Users/stacy/Desktop/IESA Project - Europe/IESA Phase 2/ners/displacy/index.html', 'w') as data:
        data.write(html)

    print('\n' + results)

    # end program
    print('Done.')

if __name__ == '__main__' : main()
