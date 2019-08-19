#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+

# IMPORTS  =====================================
import os
import sys
import spacy
from spacy import displacy
import csv
from spacy.pipeline import EntityRuler
from spacy.pipeline import Tagger
from spacy.language import Language
from pathlib import Path
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lang.en.stop_words import STOP_WORDS
import json
import pandas as pd
from pandas import ExcelWriter
import numpy as np
#from spacy.lang.en import English

# PATHS  =======================================
sys.path.append('../../../preprocessor')

# IMPORT PY FILES  =============================
import string_cleaner

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

def stemmer(d):
    pass

def entRuler_tagger(doc):
   # do something to the doc here
   pass

def update_meta_pipeline():
    pass

def combine_pattern_files(mpns, brnds):
    outFile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\output\out_mpn_brnd_patterns.jsonl'
    #print(outFile)
    of = open(outFile, 'wt')
    mpnFile = open (mpns, 'rt')
    brndFile = open(brnds, 'rt')
    for line in mpnFile:
        of.writelines(line)
        #print('.', end='', flush=True) # rem flush the output buffer
    for line in brndFile:
        of.writelines(line)
        #print('.', end='', flush=True) # rem flush the output buffer
    mpnFile.close()
    brndFile.close()
    of.close()

    return outFile

# MAIN  ========================================
def main():
    '''
    NERS Demo w/ Sample Data
    '''
    # CONFIG  ---------------------- \\
    # -------------------------------- \\
    # brnd, mpn, spplr
    model = 'pre'   # pre -> use non-trained model / post -> use trained model
    mpn = 'off'  # on/off
    brnd = 'on'  # on/off
    ruler = 'on'
    cleaner = 'on'
    number_tagger = 'off'

    # rem if stemmer is turned on after model does P2 training, then
    # you will need to use POS tag to detect nouns in products
    # then create new generator patterns for all.json
    # then run entity ruler again
    stemmer = 'off'

    # declare inputs / outputs
    brnd_pandas_file = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\output\out_brnd_pandas.xlsx'  # output
    mpn_pandas_file = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\output\out_mpn_pandas.xlsx'  # output
    mpn_file = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\input\mpn_ners_patterns.jsonl'  # input
    brnd_file = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\input\brnd_ners_patterns.jsonl'  # input

    if mpn == 'off' and brnd == 'off':
        patterns_file = mpn_file
    if mpn == 'on' and brnd == 'off':
        patterns_file = mpn_file
    elif mpn == 'off' and brnd == 'on':
        patterns_file = brnd_file
    elif mpn == 'on' and brnd == 'on':
        patterns_file = combine_pattern_files(mpn_file, brnd_file)

    tender_file = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\master\Data for Test MR 13082019.csv'
    #output_file = 'demo_ners_output_nonstock.txt'
    write_type = 'w'

    # -------------------------------- //
    # ------------------------------ //

    # load model
    if model == 'pre':
        # load a language and invoke the entity ruler
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) #('en_core_web_sm', disable=['parser'])
    elif model == 'post':
        nlp = spacy.load('model_entRuler')

    nlp.add_pipe(sentence_segmenter, after='tagger')

    # add pipes
    if ruler == 'on':
        # rem if model is post then the entity ruler is already in the model
        if model == 'pre':
            # load patterns from external file only if model is not already trained
            nu_ruler = EntityRuler(nlp).from_disk(patterns_file)
            # putting the ruler before ner will override ner decisions in favor of ruler patterns
            nlp.add_pipe(nu_ruler)#, before='ner')
        # remember to swap precedence between ruler and ner after model training
        if model == 'post':
            # load patterns from external file only if model is not already trained
            if "entity_ruler" not in nlp.pipe_names:
                nu_ruler = EntityRuler(nlp).from_disk(patterns_file)
                # putting the ner before ruler will override favor ner decisions
                nlp.add_pipe(nu_ruler)#, before='ner')

    # show pipeline components:
    print(nlp.pipe_names)

    # import test tender and clean it up
    tender = import_csv(tender_file)  # import
    if cleaner == 'on':
        tender = string_cleaner.clean_doc(tender)  #  clean

    doc = nlp(tender)

    # CONSOLE OUTPUT  ---------------------------------------------------------
    if mpn == 'on' and brnd == 'off':
        print('\n')
        labels = ['MPN']  # , 'PRODUCT', 'MPN', 'SKU']
        alt_labels = ['Mpn']  # , 'Product', 'MfrPartNo', 'SkuID']
        total_found = []
        total_unique_found = []
        for label in labels:
            print('Results for {} --------------'.format(label))
            tot_num = 0
            unique_num = 0
            unique = []
            for ent in doc.ents:
                if ent.label_ == label:
                    if ent.text not in unique:
                        unique.append(ent.text)
                        unique_num += 1
                    print([ent.text, ent.label_], end='')
                    tot_num += 1
            print('\nFound {} total, {} unique.\n'.format(tot_num, unique_num))
            total_found.append(tot_num)
            total_unique_found.append(unique_num)

    if mpn == 'off' and brnd == 'on':
        print('\n')
        labels = ['BRND']  # , 'PRODUCT', 'MPN', 'SKU']
        alt_labels = ['Brnd']  # , 'Product', 'MfrPartNo', 'SkuID']
        total_found = []
        total_unique_found = []
        for label in labels:
            print('Results for {} --------------'.format(label))
            tot_num = 0
            unique_num = 0
            unique = []
            for ent in doc.ents:
                if ent.label_ == label:
                    if ent.text not in unique:
                        unique.append(ent.text)
                        unique_num += 1
                    print([ent.text, ent.label_], end='')
                    tot_num += 1
            print('\nFound {} total, {} unique.\n'.format(tot_num, unique_num))
            total_found.append(tot_num)
            total_unique_found.append(unique_num)

    if mpn == 'on' and brnd == 'on':
        print('\n')
        labels = ['BRND', 'MPN']  # , 'PRODUCT', 'MPN', 'SKU']
        alt_labels = ['Brnd', 'Mpn']  # , 'Product', 'MfrPartNo', 'SkuID']
        total_found = []
        total_unique_found = []
        for label in labels:
            print('Results for {} --------------'.format(label))
            tot_num = 0
            unique_num = 0
            unique = []
            for ent in doc.ents:
                if ent.label_ == label:
                    if ent.text not in unique:
                        unique.append(ent.text)
                        unique_num += 1
                    print([ent.text, ent.label_], end='')
                    tot_num += 1
            print('\nFound {} total, {} unique.\n'.format(tot_num, unique_num))
            total_found.append(tot_num)
            total_unique_found.append(unique_num)

    # pandas output for mpns  ------------------------------------------------
    # This technique allows you to isolate entities on
    # a sentence-by-sentence basis, which will allow
    # for matching entities on a record-by-record basis
    if mpn == 'on':
        w_MpnCodes = []
        w_MpnCode_Alts = []
        unique = []
        mpn = ''
        alts = ''
        #ent_exists = False
        j = 0
        for sent in doc.sents:
            i = 0
            for ent in sent.ents:
                # ignore header record
                if j > 0:
                    if ent.label_ == 'MPN':
                        if i == 0:
                            # if it's the first label in the record, save it in mpns
                            mpn = ent.text
                            unique.append(ent.text)
                            i += 1
                        else:
                            # if it's not the first label in the sentence, put it in mpn alts
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
                w_MpnCodes.append(mpn.upper())
                w_MpnCode_Alts.append(alts.upper())

                # test ---------------
                print('str ', j, 'w_MpnCodes: ', w_MpnCodes)
                print('str ', j, 'w_MpnCode_Alts: ', w_MpnCode_Alts)
                # test ---------------

            # reset vars for next record
            unique.clear()
            mpn = ''
            alts = ''
            j += 1

        df = pd.DataFrame({ 'w_MpnCodes':w_MpnCodes,
                            'w_MpnCode_Alts':w_MpnCode_Alts})

        writer = pd.ExcelWriter(mpn_pandas_file)
        df.to_excel(writer,'NERS_MPNs', index=False)
        writer.save()

    # pandas output for brnds  ------------------------------------------------
    # This technique allows you to isolate entities on
    # a sentence-by-sentence basis, which will allow
    # for matching entities on a record-by-record basis
    if brnd == 'on':
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
                print('str ', j, 'w_Brnds: ', w_Brnds)
                print('str ', j, 'w_Brnd_Alts: ', w_Brnd_Alts)
                # test ---------------

            # reset vars for next record
            unique.clear()
            brnd_val = ''
            alts = ''
            j += 1

        df2 = pd.DataFrame({ 'w_Brnds':w_Brnds,
                            'w_Brnd_Alts':w_Brnd_Alts})

        writer2 = pd.ExcelWriter(brnd_pandas_file)
        df2.to_excel(writer2,'NERS_Brnds', index=False)
        writer2.save()


    # save the model  --------------------------------------------------------
    # save model with entity pattern updates made by the entity ruler
    if ruler == "on":
        output_dir = Path('model_entRuler')
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
    header = 'Named Entities Found in Tender\n'
    doc = nlp(header + spacer + results + spacer + tender)

    colors = {
        "MPN": "#C3FFA1",
        "BRND": "#FFDDA1",
    }
    options = {"ents": ["MPN", "BRND"], "colors": colors}
    # displacy.serve(doc, style="ent", options=options)
    html = displacy.render(doc, style="ent", page=True, options=options)  # use the entity visualizer
    # write the html string to the xampp folder and launch in browser through localhost port
    with open('C:/Users/stacy/My Localhost/index.html', 'w') as data:
        data.write(html)

    print('\n' + results)

    # end program
    print('Done.')

if __name__ == '__main__' : main()
