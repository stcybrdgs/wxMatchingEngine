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

                    # populate sku patterns
                    if j == 2:
                        row[j] = row[j].strip()  # strip leading and trailing whitespace from supplier string
                        sku_pattern = ''
                        sku_prefix = '{"label":"sku","pattern":[{"lower":"'
                        sku_inner = ''
                        sku_suffix = '"}]}'
                        for char in row[j]:
                            sku_inner = sku_inner + char.lower()
                        sku_pattern = sku_prefix + sku_inner + sku_suffix

                        # detect duplicates and append only unique patterns
                        # to the patterns list
                        pattern_exists = False
                        for pattern in sku_patterns:
                            if sku_pattern == pattern:
                                pattern_exists = True
                        if not pattern_exists:
                            sku_patterns.append(sku_pattern)

                    # populate supplier patterns
                    if j == 3:
                        row[j] = row[j].strip()  # strip leading and trailing whitespace from supplier string
                        supplier_pattern = ''
                        supplier_prefix = '{"label":"SUPPLIER","pattern":[{"lower":"'
                        supplier_inner = ''
                        supplier_suffix = '"}]}'
                        for char in row[j]:
                            if char == ' ':
                                supplier_inner = supplier_inner + '"},{"lower":"'
                            else:
                                supplier_inner = supplier_inner + char.lower()
                        supplier_pattern = supplier_prefix + supplier_inner + supplier_suffix

                        # detect duplicates and append only unique patterns
                        # to the patterns list
                        pattern_exists = False
                        for pattern in supplier_patterns:
                            if supplier_pattern == pattern:
                                pattern_exists = True
                        if not pattern_exists:
                            supplier_patterns.append(supplier_pattern)

                    # populate mpn patterns
                    if j == 4:
                        # prepare patterns
                        row[j] = row[j].strip()  # strip leading and trailing whitespace from supplier string
                        mpn_pattern = ''
                        mpn_prefix = '{"label":"MPN","pattern":[{"lower":"'
                        mpn_inner = ''
                        mpn_suffix = '"}]}'
                        for char in row[j]:
                            mpn_inner = mpn_inner + char.lower()
                        mpn_pattern = mpn_prefix + mpn_inner + mpn_suffix

                        # detect duplicates and append only unique patterns
                        # to the patterns list
                        pattern_exists = False
                        for pattern in mpn_patterns:
                            if mpn_pattern == pattern:
                                pattern_exists = True
                        if not pattern_exists:
                            mpn_patterns.append(mpn_pattern)

                    # populate product patterns
                    # rem this block is dependent on mpn_numbers, so it needs to
                    # follow the block where 'if j == 4:'
                    if j == 1:
                        row[j] = row[j].strip()  # strip leading and trailing whitespace from product string
                        product_pattern = ''
                        product_prefix = '{"label":"PRODUCT","pattern":[{"lower":"'
                        product_inner = ''
                        product_suffix = '"}]}'

                        # remove supplier from product detail
                        loc_first_space = row[j].find(' ')
                        length = len(row[j])
                        row[j] = row[j][loc_first_space:length].strip()

                        # remove trailing mpn from product detail
                        loc_last_space = row[j].rfind(' ')
                        row[j] = row[j][0:loc_last_space].strip()

                        # remove leading mpn from product detail
                        loc_first_space = row[j].find(' ')
                        if row[j][0:loc_first_space] == row[4]:
                            row[j] = row[j][loc_first_space:len(row[j])].strip()

                        for char in row[j]:
                            # remove commas
                            if char == ',':
                                char = ' '

                            # determine string for product_inner
                            if char == ' ':
                                # replace whitespace with pattern string
                                product_inner = product_inner + '"},{"lower":"'
                            else:
                                product_inner = product_inner + char.lower()
                        product_pattern = product_prefix + product_inner + product_suffix

                        # detect duplicates and append only unique patterns
                        # to the patterns list
                        pattern_exists = False
                        for pattern in product_patterns:
                            if product_pattern == pattern:
                                pattern_exists = True
                        if not pattern_exists:
                            product_patterns.append(product_pattern)

                    j += 1

            # populate txt obj
            doc = doc + ('|'.join(row) + '\n')
            i += 1

    # create pattern files using jsonl
    # supplier patterns:
    with open('ners_patterns_supplier.jsonl', 'w') as outfile:
        for line in supplier_patterns:
            outfile.write(line + '\n')

    # mpn patterns:
    with open('ners_patterns_mpn.jsonl', 'w') as outfile:
        for line in mpn_patterns:
            outfile.write(line + '\n')

    # sku patterns
    with open('ners_patterns_sku.jsonl', 'w') as outfile:
        for line in sku_patterns:
            outfile.write(line + '\n')

    # product patterns
    with open('ners_patterns_product.jsonl', 'w') as outfile:
        for line in product_patterns:
            outfile.write(line + '\n')

    # base nlp on blank Language class
    nlp = spacy.blank("en")  # create blank Language class

    # create nlp obj
    b_doc = nlp(doc)

    # end program
    print('Done.')

if __name__ == '__main__' : main()
