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

    model = 'post'   # pre -> use non-trained model / post -> use trained model
    ruler = 'on'
    cleaner = 'on'
    number_tagger = 'off'
    # if stemmer is turned on after model does P2 training, then
    # you will need to use POS tag to detect nouns in products
    # then create new generator patterns for all.json
    # then run entity ruler again
    stemmer = 'off'

    # --------------------------------
    # load model
    if model == 'pre':
        # load a language and invoke the entity ruler
        nlp = spacy.load('en_core_web_sm', disable=['parser']) #('en_core_web_sm', disable=['parser'])
    elif model == 'post':
        nlp = spacy.load('model_entRuler')
        #nu_pipe = nlp.create_pipe('my_pipe')
        #tagger = Tagger(nlp.vocab)
        #tagger = tagger.from_disk('model_entRuler')
        #nlp.add_pipe(nlp.create_pipe(tagger))
        #Language.factories['entRuler_tagger'] = lambda nlp, **cfg: EntityMatcher(nlp, **cfg)
        #entRuler_tagger = Tagger(nlp.vocab)
        #entRuler_tagger = entRuler_tagger.from_disk('model_entRuler/tagger')
        #nlp.add_pipe(entRuler_tagger, first = True)
        #tagger = nlp.create_pipe('tagger')

    # add pipes
    if ruler == 'on':
        # rem if model is post then the entity ruler is already in the model
        if model == 'pre':
            # load patterns from external file only if model is not already trained
            nu_ruler = EntityRuler(nlp).from_disk('ners_patterns_all.jsonl')
            # putting the ruler before ner will override ner decisions in favor of ruler patterns
            nlp.add_pipe(nu_ruler, before='ner')
        # remember to swap precedence between ruler and ner after model training
        if model == 'post':
            # load patterns from external file only if model is not already trained
            if "entity_ruler" not in nlp.pipe_names:
                nu_ruler = EntityRuler(nlp).from_disk('ners_patterns_all.jsonl')
                # putting the ner before ruler will override favor ner decisions
                nlp.add_pipe(nu_ruler, after='ner')

            # write tagger into pipeline in the meta json file
            # STOPPED HERE ------------------------

    # show pipeline components:
    print(nlp.pipe_names)

    # import test tender and clean it up
    tender = import_csv('iesa_tender.csv')  # import
    if cleaner == 'on':
        tender = string_cleaner.clean_doc(tender)  #  clean

    doc = nlp(tender)

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
