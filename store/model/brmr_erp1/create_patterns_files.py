#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
'''
Sunday, July 7, 2019
Stacy Bridges
'''
# IMPORT LIBS  =================================
import spacy
import csv
import sys
import os

# SYS PATH  ====================================
#sys.path.append('../../../preprocessor/')

# IMPORT PY FILES  =============================
#import loader

# GLOBALS  =====================================

# FUNCTIONS  ===================================

# MAIN  ========================================
def main():
    # declare containers
    hash_ids = []
    header_names = []
    supplier_patterns = []

    # store\model\brmr_erp1\brmr_erp1.csv
    brmr_csv = '../../../store/model/brmr_erp1/brmr_erp1.csv'

    # import brammer csv
    #d = import_csv(brmr_csv)
    doc = ''
    with open(brmr_csv) as data:
        csv_reader = csv.reader(data, delimiter='|')
        i = 0
        for row in csv_reader:
            # populate header_names[]
            if i == 0:
                j = 0
                for field in row:
                    header_name = row[j]
                    header_names.append(header_name)
                    j += 1

            # get hash ids and create pattern files
            if i > 0:  # skip header row
                j = 0
                for field in row:
                    # populate hash_ids[]
                    if j == 0:
                        hash_id = row[j].strip()
                        hash_ids.append(hash_id)
                    # end if //

                    # populate supplier patterns
                    if j == 3:
                        row[j] = row[j].strip()  # strip leading and trailing whitespace from supplier string
                        supplier_prefix = '{"label":"SUPPLIER","pattern":[{"lower":"'
                        supplier_pattern = ''
                        supplier_suffix = '"}]}'
                        supplier_inner = ''
                        for char in row[j]:
                            if char == ' ':
                                supplier_inner = supplier_inner + '"},{"lower":"'
                            else:
                                supplier_inner = supplier_inner + char
                        supplier_pattern = supplier_prefix + supplier_inner + supplier_suffix

                        # detect duplicates so as to only append unique patterns
                        # to the supplier patterns list
                        pattern_exists = False
                        for pattern in supplier_patterns:
                            if supplier_pattern == pattern:
                                pattern_exists = True
                        if not pattern_exists:
                            supplier_patterns.append(supplier_pattern)
                    j += 1

            # populate txt obj
            doc = doc + ('|'.join(row) + '\n')
            i += 1

    # test print
    #print(d)

    # base nlp on blank Language class
    nlp = spacy.blank("en")  # create blank Language class

    # create nlp obj
    b_doc = nlp(doc)

    # test  ---------------------------\\
    #                                   \\
    i = 0
    for tok in b_doc:
        if i > 50: break
        print([tok.text])
        i += 1

    print(hash_ids)
    print(header_names)
    print('supplier_prefix: ', supplier_prefix)
    print('supplier_inner: ', supplier_inner)
    print('supplier_suffix: ', supplier_suffix)
    print('supplier_pattern: ' , supplier_pattern)
    print('--------------- Supplier Patterns: ---------------')
    for item in supplier_patterns:
        print(item)

    # print supplier patterns to jsonl file
    with open('ners_supplier_patterns.jsonl', 'w') as outfile:
        for line in supplier_patterns:
            outfile.write(line + '\n')




    #                                   //
    # test  ---------------------------//

    # break out mpn

    # break out products

    # break out sku

    # break out



    # end program
    print('Done.')

if __name__ == '__main__' : main()
