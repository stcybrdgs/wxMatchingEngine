# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16
@author: Stacy Bridges

these scripts test the functions needed to create an annotated
nlp object from a csv product group. the pumps group is used for this code set.

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
after the nlp object is created, the array data is used to create custom
annotations for the corresponding tokens/spans. then, the tokens/spans for
product and supplier are used to locate the strings that need to be further
annotated with phonetic encodings for soundex and nysiis.

storing:    -------------------
the final version of the nlp object is saved as a pickle so that it can
be imported into the match engine when necessary to compare against new
data for the use cases (1) erp vs mdm; and (2) tender vs erp

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

        # TEST list
        print('contents of arrays for tagging:\n')
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
            txt_obj = txt_obj + ' '.join(row) + '.\n'
            i += 1

    # TEST print
    for item in testList:
        print(item)

    # clean the text object
    txt_obj = preprocessor.string_cleaner(txt_obj)

    # TEST PRINT
    print('\n\ntxt_obj after cleaning:\n', txt_obj)

    # create the nlp object:
    pumps_erp10 = nlp(txt_obj)

    # TEST print
    print('\n\npumps_erp10 after sentencizer:\n')
    for sent in pumps_erp10.sents:
        print(sent.text, '**End Row**', end='')


    print('\nDone.')

if __name__ == '__main__' : main()
