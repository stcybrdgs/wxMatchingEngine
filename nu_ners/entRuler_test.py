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
    #global row_heads
    doc = ''
    with open(d) as data:
        csv_reader = csv.reader(data, delimiter='|')
        i = 0
        for row in csv_reader:
            # populate row_heads[]
            #if i > 0:  # skip header row
            #row_head = row[0]
            #row_heads.append(row_head)
            # populate txt obj
            if i == 0:
                # add top anchor to keep displacy from collapsing
                doc = doc + 'wrwxstart ' + ('|'.join(row) + '\n')
            else:
                doc = doc + 'wrwx ' + ('|'.join(row) + '\n')
            i += 1

    # add bottom anchor to keep displacy from collapsing
    doc = doc + 'wrwxend ' + ('|'.join(row) + '\n')
    return doc
    # end function //

# MAIN  ===========================================
def main():
    test_mpns = [
        '040/1.0',
        '1/2/3-PIN/FEMALE',
        '040"/1.0',
        '1/2"/3-PIN/FEMALE',
        '1577340000',
        'BR1200GI',
        '40.31.8.230.0000',
        '40.52.8.110.0000',
        '40/31',
        '6EP1436-3BA00',
        '60.13.8.230.0040',
        '6AV2124-0QC02-0AX0',
        'M22-DP-R-X0+M22-A',
        'P1-25/EA/SVB',
        'CR2032',
        'EOC/5',
        '239.46+16',
        'P1000 (P1001)',
        'P10/00',
        'P 1796',
        'PS\\02\\53'
    ]

    #tender = ''
    #for num in test_mpns:
    #    tender = tender + num.lower() + '\n'

    #sys.exit()

    # load model
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) #('en_core_web_sm', disable=['parser'])
    #elif model == 'post':nlp = spacy.load('demo_model')
    nlp.add_pipe(sentence_segmenter, after='tagger')

    # add pipes
    #if ruler == 'on':
    # load patterns from external file only if model is not already trained
    patterns_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_db_mpn_delme_test_patterns.jsonl'
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

    # ask user to select a column from the user-selected data file
    # and turn it into a csv file that can be imported by NERS
    #tender_col_csv = create_tender_csv(tender_file)  # create the csv and return csv filename
    #tender = import_csv(tender_col_csv)  # import the csv

    tender_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\db_mpn_delme_test.csv'
    tender = import_csv(tender_file)
    tender = tender.lower()

    #print(tender)
    #sys.exit()

    doc = nlp(tender)

    for sent in doc.sents:
        for tok in sent:
            print('{}{}'.format(tok.text, '^'))

    for sent in doc.sents:
        for ent in sent.ents:
            print(ent.text, ' | ', ent.label_)


    # end program
    print('Done.')

if __name__ == '__main__' : main()
