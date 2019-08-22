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
    # CONFIG  -------------------------------------------------- \\
    # ------------------------------------------------------------ \\

    # set parameters to run either MPN or BRND (only one choice per run)
    dataLabel = 'CMMDTY'  # MPN, BRND, SPPLR, CMMDTY

    pattern_generator_inpath = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\input'
    pattern_generator_outpath = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\input'

    # ------------------------------------------------------------ //
    # ---------------------------------------------------------- //

    if dataLabel == 'MPN':
        dataIn = r'\in_mpn.csv'  # in_MPN.csv or in_BRND.csv
        ners_patterns = r'\mpn_ners_patterns.jsonl'  # out_MPN.jsonl or out_BRND.jsonl
    elif dataLabel == 'BRND':
        dataIn = r'\in_brnd.csv'  # in_MPN.csv or in_BRND.csv
        ners_patterns = r'\brnd_ners_patterns.jsonl'  # out_MPN.jsonl or out_BRND.jsonl
    elif dataLabel == 'SPPLR':
        dataIn = r'\in_spplr.csv'  # in_MPN.csv or in_BRND.csv
        ners_patterns = r'\spplr_ners_patterns.jsonl'  # out_MPN.jsonl or out_BRND.jsonl
    elif dataLabel == 'CMMDTY':
        dataIn = r'\in_cmmdty.csv'  # in_MPN.csv or in_BRND.csv
        ners_patterns = r'\cmmdty_ners_patterns.jsonl'  # out_MPN.jsonl or out_BRND.jsonl

    # parameters
    infile  =  pattern_generator_inpath + dataIn
    outfile =  pattern_generator_outpath + ners_patterns

    # declare containers
    patterns = []

    # import erp csv
    doc = ''
    with open(infile) as data:
        csv_reader = csv.reader(data, delimiter = '|')
        i = 0
        for line in csv_reader:
            if i > 0:  # skip header row
                # populate patterns
                pattern = ''
                prefix = '{"label":"' + dataLabel + '", "pattern":[{"lower":"'
                inner = ''
                suffix = '"}]}'
                for char in line:
                    if char == ' ':
                        inner = inner + '"},{"lower":"'
                    else:
                        inner = inner + char.lower()
                pattern = prefix + inner + suffix + '\n'

                # detect duplicates and append only unique patterns
                # to the patterns list
                pattern_exists = False
                for p in patterns:
                    if p == pattern:
                        pattern_exists = True
                if not pattern_exists:
                    patterns.append(pattern)
            i += 1

    # create pattern files using jsonl
    # supplier patterns:
    with open(outfile, 'w') as outfile:
        for line in patterns:
            outfile.write(line)
            print(line)

    # end program
    print('Done.')

if __name__ == '__main__' : main()
