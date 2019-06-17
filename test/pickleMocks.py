# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16
@author: Stacy

"""
# IMPORTS  =========================================
import csv
import spacy
from spacy.lang.en.examples import sentences

# FUNCTIONS  =======================================

def main():
    nlp = spacy.load('en_core_web_sm')

    #txt_file = input('../store/model/erp10/pumps/prod_pumps_erp10.txt')
    csv_path = '../store/model/erp10/pumps/prod_pumps_erp10.csv'
    txt_obj = ''
    with open (csv_path) as data:
        reader = csv.reader(data, delimiter =' ', quotechar = ' ',
                            quoting = csv.QUOTE_MINIMAL)
        for row in reader:
            txt_obj = txt_obj + ' '.join(row) + '\n'

    print(txt_obj)

    pumps_erp10 = nlp(txt_obj)


    '''
    with open(txt_file, "w") as my_output_file:
        my_output_file.write("#1\n")
        my_output_file.write("double({},{})\n".format(len(text_list), 2))
        for line in text_list:
            my_output_file.write("  " + line)
        print('File Successfully written.')
    '''
    '''
    with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as data:
        docObj = csv.reader(data, delimiter='|')
        for row in docObj:
            print(row)

    # create model ------------------
    # get doc
    '''
    '''
    with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as infile:
        fileObj = csv.reader(infile, delimiter='|')
        doc = ''
        for row in fileObj:
            print(row)
    '''
    '''
    csv_reader = csv.DictReader(csv_file)
    '''
    '''
    data = ''
    with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as data:
        data = csv.reader(data, delimiter='|')
        headers = []
        productIDs = []
        products = []
        suppliers = []
        mpns = []
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
    print(headers)
    print(productIDs)
    '''
    '''
    print('csv_reader: \n')
    for row in csv_reader:
        print(row)
    print('headers: \n', headers)
    '''
    '''
    # clean the test string
    doc = preprocessor.string_cleaner(doc)
    print('/nstring clean doc:/n', doc)

    # create nlp object from test string
    processor.create_nlp_object(doc)
    '''



    print('Done.')

if __name__ == '__main__' : main()
