#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
'''
Sunday, July 19, 2019
Stacy Bridges

'''
# IMPORT LIBS  =================================
import spacy
import csv

# MAIN  ========================================
def main():
    # declare containers
    supplier_patterns = []

    # store\model\brmr_erp1\brmr_erp1.csv
    demo_txt = '../../../store/model/brmr_erp1/demo_ners_mmat_lookup.csv'
    #brmr_csv = '../../../store/model/brmr_erp1/nu_iesa_erp/iesa_erp_nu.csv'

    # import erp csv
    doc = ''
    with open(demo_txt) as data:
        csv_reader = csv.reader(data, delimiter = '|')
        i = 0
        for line in csv_reader:
            if i > 0:  # skip header row
                # populate supplier patterns
                #line[0].strip()  # strip leading and trailing whitespace from supplier string
                supplier_pattern = ''
                supplier_prefix = '{"label":"MMAT","pattern":[{"lower":"'
                supplier_inner = ''
                supplier_suffix = '"}]}'
                for char in line:
                    if char == ' ':
                        supplier_inner = supplier_inner + '"},{"lower":"'
                    else:
                        supplier_inner = supplier_inner + char.lower()
                supplier_pattern = supplier_prefix + supplier_inner + supplier_suffix + '\n'
                #print(supplier_pattern)

                # detect duplicates and append only unique patterns
                # to the patterns list
                pattern_exists = False
                for pattern in supplier_patterns:
                    if supplier_pattern == pattern:
                        pattern_exists = True
                if not pattern_exists:
                    supplier_patterns.append(supplier_pattern)
                    #print(supplier_pattern)
            i += 1

        '''
        # populate txt obj
        doc = doc + ('|'.join(row) + '\n')
        i += 1
        '''

    # create pattern files using jsonl
    # supplier patterns:
    with open('demo_ners_patterns_mmat.jsonl', 'w') as outfile:
        for line in supplier_patterns:
            outfile.write(line)
            print(line)

    # end program
    print('Done.')

if __name__ == '__main__' : main()
