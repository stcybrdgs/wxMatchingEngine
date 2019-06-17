# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16
@author: Stacy Bridges

these scripts test the functions needed to create an annotated
nlp object from a csv product group. the pumps group is used for this code set.

importing:  ------------------
    the csv is imported twice:
    on the first import, the data is captured in list format so that the
    arrays can be used to capture:
        - productID
        - product
        - supplier
        - mpn

    on the second import, the data is captured in string format as a text
    object that can be turned into an nlp object.

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
import csv
import spacy
from spacy.lang.en.examples import sentences

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

# FUNCTIONS  =======================================

def main():
    nlp = spacy.load('en_core_web_sm')

    # import csv -- first pass
    # get product group data file and feed the info into a text object
    with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as data:
        data = csv.reader(data, delimiter='|')
        headers = []
        productIDs = []
        products = []
        suppliers = []
        mpns = []

        # TEST list
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
            i += 1
    # TEST print
    for item in testList:
        print(item)

    print('Done.')

if __name__ == '__main__' : main()
