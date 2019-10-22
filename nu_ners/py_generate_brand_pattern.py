#!/usr/bin/env python
# coding: utf8
"""
Mon, OCt 21, 2019
Stacy Bridges

This simplified code transforms an input set of brands into brand patterns
for the NERS EntityRuler.

"""
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

'''
# test data  -----------------------------------------------
brands = ['3M','A & A','A K FLUIDTECH','AAF',
    'AAK BALERY','ACCU-CODER','PEPPERL&FUCHS',
    'PEPPERL & FUCHS','PEPPERL+FUCHS','PEPPERL + FUCHS'
]
'''

outfile = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_patterns_brnd.jsonl'
brands_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\in_brnd.xlsx'
brands_sheet = 'in_brnd'
brands_data = pd.read_excel(brands_file, brands_sheet)
brands = brands_data['BRAND']
dataLabel = 'BRND'

# declare variables  ---------------------------------------------
# special chars
special_chars = [' ','/','\\','+','-','.','&',',','(',')']

# pattern components
pp = '{"label":"' + dataLabel + '", "pattern":['  # pp = pattern prefix
ps = ']}'  # ps = pattern suffix
patterns = []
pattern = ''

# token components
tp = '{"lower":"'  # token prefix
ts = '"}' # token suffix
td = ',' # token delimiter
tokens = []
token = ''

# build brand patterns  ------------------------------------------
# iterate thru brands to build patterns from the pattern and token components above
for brand in brands:
    brand = str(brand)  # eliminate any float objects
    char_count = 0
    is_last_char = False

    for char in brand:
        char_count += 1
        if char_count == len(brand):
            is_last_char = True

        if char in special_chars:
            if token != '':
                tokens.append(token)
                token = ''
            if char == ' ':
                char = ''
            tokens.append(char)
        else:
            token = token + char

        if is_last_char == True:
            tokens.append(token)
            token = ''

    # after iterating through the brand string, build the pattern
    pattern = pattern + pp
    tok_count = 0
    is_last_token = False
    for tok in tokens:
        tok_count += 1
        if tok_count == len (tokens):
            is_last_token = True

        if is_last_token == False:
            pattern = pattern + tp + tok + ts + td
        else:
            pattern = pattern + tp + tok + ts

    pattern = pattern + ps
    patterns.append(pattern)
    pattern = ''
    tokens.clear()

# write brand patterns to file  -------------------------------
brand_count = 0
with open(outfile, 'w') as outfile:
    for line in patterns:
        outfile.write(line)
        outfile.write('\n')
        print(line)
        brand_count += 1

# end program
print('{} brand patterns written to JSONL file'.format(brand_count))
print('Done.')
