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
import pickle
#from spacy.lang.en import English

# PATHS  =======================================
sys.path.append('../../../preprocessor/')
sys.path.append('../../../processor/')

# IMPORT PY FILES  =============================
import string_cleaner
import update_meta_json
# import nlp_object_processor

# GLOBALS  =====================================
global row_heads
row_heads = []

# FUNCTIONS  ===================================
def sentence_segmenter(doc):
    # get the list of row heads
    # row_heads = loader.get_row_heads()
    global row_heads

    j = 0
    # normalize row heads so that they can be compared to text in nlp obj
    '''
    for rh in row_heads:
        row_heads[j] = string_cleaner.normalizer(rh)
        j += 1
    '''

    # set each row head as a sentence start
    j = 0
    for rh in row_heads:
        for token in doc:
            if token.text == rh:
                doc[token.i].is_sent_start = True
        j += 1

    return doc
    # end function //

def make_pickle(d):
    f = "tender.pickle"
    pickling_on = open(f,"wb")
    pickle.dump(d, pickling_on)
    pickling_on.close()
    #return f

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

def stemmer(d):
    pass

def entRuler_tagger(doc):
   # do something to the doc here
   pass

def update_meta_pipeline():
    '''
    json_content = []
    old_pipeline = []
    nu_pipeline = ['tagger', 'entity_ruler', 'ner']

    # read in meta.json
    with open('model_entRuler/meta.json','r') as jsonfile:
        json_content = json.load(jsonfile)
        old_pipeline = json_content['pipeline']

    if nu_pipeline == old_pipeline:
        pass
    else:
        # update json_content to reflect new pipeline
        json_content['pipeline'] = nu_pipeline

        # write the new pipeline to the json file
        with open('model_entRuler/meta.json','w') as jsonfile:
            json.dump(json_content, jsonfile)
    '''
    pass

# MAIN  ========================================
def main():
    '''
    NERS Demo
    IESA Sample Data
    '''
    # CONFIG  ------------------------

    model = 'pre'   # pre -> use non-trained model / post -> use trained model
    ruler = 'off'
    cleaner = 'off'
    number_tagger = 'off'
    stemmer = 'off'

    # --------------------------------
    # load model
    if model == 'pre':
        # load a language and invoke the entity ruler
        nlp = spacy.load('en_core_web_sm', disable=['parser']) #('en_core_web_sm', disable=['parser'])
    elif model == 'post':
        update_meta_json.update_meta()
        nlp = spacy.load('model')

    # add pipes
    if ruler == 'on':
        if "entity_ruler" not in nlp.pipe_names:
            nu_ruler = EntityRuler(nlp).from_disk('ners_patterns_all.jsonl')
            # putting the ner before ruler will override favor ner decisions
            if model == 'pre':
                nlp.add_pipe(nu_ruler, before='ner')
            else:
                nlp.add_pipe(nu_ruler, after='ner')

    nlp.add_pipe(sentence_segmenter, before='ner')

    # show pipeline components:
    print(nlp.pipe_names)

    # import test tender and clean it up
    tender = import_csv('iesa_tender.csv')  # import
    if cleaner == 'on':
        tender = string_cleaner.clean_doc(tender)  #  clean

    doc = nlp(tender)

    # this nlp tender obj is cleaned -- pickle it
    make_pickle(doc)


    # CONSOLE OUTPUT
    print('\n')
    labels = ['SUPPLIER', 'PRODUCT', 'MPN', 'SKU']
    alt_labels = ['Supplier', 'Product', 'MfrPartNo', 'SkuID']
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

    # save model with entity pattern updates made by the entity ruler

    if ruler == "on":
        output_dir = Path('model')
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
    for i in suppliers:
        print(i)
    print('--------------------------')
    for i in products:
        print(i)
    print('--------------------------')
    for i in mpns:
        print(i)
    print('--------------------------')
    for i in skus:
        print(i)

    # DISPLACY VISUALIZER
    # get results for html doc
    results = ''
    i = 0
    for item in alt_labels:
        results = results + '{}: {} tot  {} unq\n'.format(item, total_found[i], total_unique_found[i])
        i += 1
    # store nlp object as string in html var
    spacer = '---------------------------------------------------------\n'
    header = 'IESA Named Entities Found in Tender\n'
    doc = nlp(header + spacer + results + spacer + tender)

    html = displacy.render(doc, style="ent", page=True)  # use the entity visualizer
    # write the html string to the xampp folder and launch in browser through localhost port
    with open('C:/xampp/htdocs/mySites/wrWx_NERS/index.html', 'w') as data:
        data.write(html)

    print('\n' + results)

    '''
    for sent in doc.sents:
        print(sent)

    for tok in doc:
        if tok.is_stop == False:
            print([tok.text, tok.pos_, tok.tag_])
    '''
    # TEST  -----------------------------

    # end program
    print('Done.')

if __name__ == '__main__' : main()
