#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+

# IMPORTS  =====================================
import os
import sys
import spacy
import csv
from spacy.pipeline import EntityRuler
from pathlib import Path
#from spacy.lang.en import English

# PATHS  =======================================
sys.path.append('../../../preprocessor/')

# IMPORT PY FILES  =============================
import string_cleaner

# GLOBALS  =====================================
global row_heads
row_heads = []

# FUNCTIONS  ===================================
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
            doc = doc + ('|'.join(row) + '\n')
            i += 1
    return doc
    # end function //

# MAIN  ========================================
def main():
    model = 'post'  # pre -> use non-trained En model
                    # post -> use the trained model

    if model == 'pre':
        # load a language and invoke the entity ruler
        nlp = spacy.load('en_core_web_sm', disable=['parser']) #English()

        # load patterns from external file
        nu_ruler = EntityRuler(nlp).from_disk('ners_patterns_all.jsonl')

        # putting the ruler before ner will override ner decisions in favor of ruler patterns
        nlp.add_pipe(nu_ruler, before='ner')
    elif model == 'post':
        nlp = spacy.load('model', disable=['parser']) #English()

    # show pipeline components:
    print(nlp.pipe_names)

    # import test tender and clean it up
    tender = import_csv('brmr_tender.csv')  # import
    tender = string_cleaner.clean_doc(tender)  #  clean

    doc = nlp(tender)

    print('\n')
    labels = ['SUPPLIER', 'PRODUCT', 'MPN', 'SKU']
    for label in labels:
        print('{} --------------'.format(label))
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
        print('\nFound {} total, {} unique\n'.format(tot_num, unique_num))

    # save model with entity pattern updates made by the entity ruler
    '''
    output_dir = Path('model_entRuler')
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)
    '''

    # end program
    print('Done.')

if __name__ == '__main__' : main()
