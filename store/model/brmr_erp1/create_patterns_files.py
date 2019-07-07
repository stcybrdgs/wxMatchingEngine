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
    # rem fields are: HashID, Product, SKU, Brand, MPN, Attr
    hash_ids = []
    header_names = []
    supplier_patterns = []
    mpn_patterns = []
    sku_patterns = []
    product_patterns = []

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

                    # populate product patterns
                    if j == 1: pass

                    # populate sku patterns
                    if j == 2:
                        row[j] = row[j].strip()  # strip leading and trailing whitespace from supplier string
                        sku_pattern = ''
                        sku_prefix = '{"label": "sku", "pattern": [{"lower":"'
                        sku_inner = ''
                        sku_suffix = '"}]}'
                        for char in row[j]:
                            sku_inner = sku_inner + char.lower()
                        sku_pattern = sku_prefix + sku_inner + sku_suffix

                        # detect duplicates and append only unique patterns
                        # to the sku patterns list
                        pattern_exists = False
                        for pattern in sku_patterns:
                            if sku_pattern == pattern:
                                pattern_exists = True
                        if not pattern_exists:
                            sku_patterns.append(sku_pattern)

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
                                supplier_inner = supplier_inner + char.lower()
                        supplier_pattern = supplier_prefix + supplier_inner + supplier_suffix

                        # detect duplicates and append only unique patterns
                        # to the supplier patterns list
                        pattern_exists = False
                        for pattern in supplier_patterns:
                            if supplier_pattern == pattern:
                                pattern_exists = True
                        if not pattern_exists:
                            supplier_patterns.append(supplier_pattern)

                    # populate mpn patterns
                    if j == 4:
                        row[j] = row[j].strip()  # strip leading and trailing whitespace from supplier string
                        mpn_pattern = ''
                        mpn_prefix = '{"label": "MPN", "pattern": [{"lower":"'
                        mpn_inner = ''
                        mpn_suffix = '"}]}'
                        for char in row[j]:
                            mpn_inner = mpn_inner + char.lower()
                        mpn_pattern = mpn_prefix + mpn_inner + mpn_suffix

                        # detect duplicates and append only unique patterns
                        # to the mpn patterns list
                        pattern_exists = False
                        for pattern in mpn_patterns:
                            if mpn_pattern == pattern:
                                pattern_exists = True
                        if not pattern_exists:
                            mpn_patterns.append(mpn_pattern)

                    j += 1

            # populate txt obj
            doc = doc + ('|'.join(row) + '\n')
            i += 1


    # test  ---------------------------\\
    #                                   \\
    '''
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

    print('--------------- MPN Patterns: ---------------')
    i = 0
    for item in mpn_patterns:
        print(item)
        i += 1
    print('mpn_patterns has {} rows'.format(i))
    '''
    #                                   //
    # test  ---------------------------//

    # create pattern files using jsonl
    # supplier patterns:
    with open('ners_supplier_patterns.jsonl', 'w') as outfile:
        for line in supplier_patterns:
            outfile.write(line + '\n')

    # mpn patterns:
    with open('ners_mpn_patterns.jsonl', 'w') as outfile:
        for line in mpn_patterns:
            outfile.write(line + '\n')

    # sku patterns
    with open('ners_sku_patterns.jsonl', 'w') as outfile:
        for line in sku_patterns:
            outfile.write(line + '\n')

    # product patterns

    # base nlp on blank Language class
    nlp = spacy.blank("en")  # create blank Language class

    # create nlp obj
    b_doc = nlp(doc)


    # end program
    print('Done.')

if __name__ == '__main__' : main()
