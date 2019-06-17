# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16
@author: Stacy Bridges

these scripts test the functions needed to create an annotated
nlp object from a csv product group.
the pumps group is used for this code set.

importing:  ------------------
    the csv data is initially captured in list format before being
    converted to a text object so that arrays can be used to capture:
        - productID
        - product
        - supplier
        - mpn
    the info in the arrays can then be used tag each corresponding token
    with custom annotations

custom tagging:    ------------
after the nlp object is created, use the array data to create custom
annotations for the corresponding tokens/spans. then, use the tokens/spans
for product and supplier to locate the strings that need to be further
annotated with phonetic encodings for soundex and nysiis.

storing:    -------------------
the final version of the nlp object is saved as a pickle so that it can
be imported into the match engine when necessary to compare against new
data for the use cases (1) erp vs mdm; and (2) tender vs erp

challenges:    -------------------
because of the nature of the product description data (ie, not syntactically or
semantically structured as expected by the language model), the pos tagger and
dependency parcer cannot identify dependencies as they normally would with
properly strucutred language. as a reuls, the spacy sentence segmenter does not
have the information it needs to correctly segment each incoming record as
a sentence. workarounds might include:
- do not import the language model
    pros:   you can then use sentencizer as a pipe component to segment
            sentences based on terminal punctuation (ie '.', '!', and '?' )
    cons:   you lose tagging for pos and ner
- go ahead an import the language model, but write your own segmentation component
    pros:   you keep tagging for pos and ner
    cons:   you have to write a segmentation component, and it is designed
            specifically to handle data sets peculiar to the target use case only

"""

# IMPORT LIBS  ======================================
import os
import sys
import re
import csv
import spacy
from spacy.lang.en import English
#from spacy.lang.en.examples import sentences

# PATHS ================================
# import importlib
# rem use importlib to import module stored as string
sys.path.append('../io/')
sys.path.append('../ners/')
sys.path.append('../preprocessor/')
sys.path.append('../processor/')
sys.path.append('../store/')

# IMPORT FUNCTIONS  =====================
#import loader
#import processor
import preprocessor
import loader

# FUNCTIONS  =======================================

def main():
    # get just the language with no model
    nlp = English()
    # nlp = spacy.load('en_core_web_sm')

    # add the sentencizer component to the pipeline
    # rem this component  splits sentences on punctuation such as . !  ?
    # plugging it into pipeline to get just the sentence boundaries
    # without the dependency parse.
    sentencizer = nlp.create_pipe("sentencizer")
    nlp.add_pipe(sentencizer)

    '''
    Model for component 'ner' not initialized.
    Did you forget to load a model, or forget to call begin_training()?
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner)
    '''

    # get product group data file and feed the info into arrays
    # that will be used later to create custom tags for the nlp object
    txt_obj = ''
    with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as data:
        data = csv.reader(data, delimiter='|')
        headers = []
        productIDs = []
        products = []
        suppliers = []
        mpns = []

        # TEST print    -----------------------
        #print('contents of arrays for tagging:\n')

        testList = [headers, productIDs,
                    products, suppliers, mpns]
        i = 0
        for row in data:
            if i == 0:
                headers.append(row)
            else:
                productID = row[0]
                product = row[1]
                supplier = row[2]
                mpn = row[3]

                productIDs.append(productID)
                products.append(product)
                suppliers.append(supplier)
                mpns.append(mpn)

            # create text object
            # rem add a period at the end so that the spacy sentencizer
            # knows how to detect the end of each record
            # and add all rows to text object except for header row
            if i != 0:
                txt_obj = txt_obj + ' '.join(row) + '.\n'
            i += 1

    # TEST print  -----------------------
    print('testList items:\n')
    for item in testList:
        print(item)

    # clean the text object
    txt_obj = preprocessor.string_cleaner(txt_obj)

    # TEST PRINT  -----------------------
    print('\n\ntxt_obj after cleaning:\n', txt_obj)

    # create the nlp object:
    pumps_erp10 = nlp(txt_obj)

    # TEST print  -----------------------
    print('\n\npumps_erp10 after sentencizer:\n')
    for sent in pumps_erp10.sents:
        print(sent.text, '**end row**', end='')

    # TEST print  -----------------------
    print('\n\ntoken.like_num in nlp obj:\n')
    for token in pumps_erp10:
        print(token.like_num,',', end='')

    # stuff we get:
    # token, .text, .i, .idx, .tag_, .lemma_
    # .is_punct, .is_space, .like_num
    print('\nDone.')

    # stuff we don't get:
    # pos, ent, chunking,

    # LU
    # textcat (TextCategorizer, Doc.cats)
    # custom components (Doc._.xxx, Token._.xxx, Span._.xxx)
    # create_pipe, add_pipe

    # TEST print  -----------------------
    print('\n', nlp.pipeline)
    print('\n', nlp.pipe_names)

if __name__ == '__main__' : main()
