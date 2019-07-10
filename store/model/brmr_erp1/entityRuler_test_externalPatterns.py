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
    model = 'pre'   # pre -> use non-trained model / post -> use trained model
    ruler = 'on'
    cleaner = 'on'

    if model == 'pre':
        # load a language and invoke the entity ruler
        nlp = spacy.load('en_core_web_sm', disable=['parser']) #English()
    elif model == 'post':
        nlp = spacy.load('model', disable=['parser']) #English()

    if ruler == 'on':
        if model == 'pre':
            # load patterns from external file only if model is not already trained
            nu_ruler = EntityRuler(nlp).from_disk('ners_patterns_all.jsonl')
            # putting the ruler before ner will override ner decisions in favor of ruler patterns
            nlp.add_pipe(nu_ruler, before='ner')

    # show pipeline components:
    print(nlp.pipe_names)

    # import test tender and clean it up
    tender = import_csv('iesa_tender.csv')  # import
    if cleaner == 'on':
        tender = string_cleaner.clean_doc(tender)  #  clean

    doc = nlp(tender)

    print('\n')
    labels = ['SUPPLIER', 'PRODUCT', 'MPN', 'SKU']
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
        print('\nFound {} total, {} unique\n'.format(tot_num, unique_num))

    # save model with entity pattern updates made by the entity ruler

    if ruler == "on":
        output_dir = Path('model_entRuler')
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

    # TEST  -----------------------------
    suppliers = []
    products = []
    skus = []
    mpns = []
    # print(doc)
    for ent in doc.ents:
        if ent.label_ in labels:
            if ent.label_ == 'SUPPLIER':
                suppliers.append([ent.label_, ent.text])
            elif ent.label_ == 'PRODUCT':
                products.append([ent.label_, ent.text])
            elif ent.label_ == 'SKU':
                skus.append([ent.label_, ent.text])
            elif ent.label_ == 'MPN':
                mpns.append([ent.label_, ent.text])

    print('--------------------------')
    for i in suppliers: print(i)
    print('--------------------------')
    for i in products: print(i)
    print('--------------------------')
    for i in skus: print(i)
    print('--------------------------')
    for i in mpns: print(i)



    # TEST  -----------------------------

    # end program
    print('Done.')

if __name__ == '__main__' : main()
