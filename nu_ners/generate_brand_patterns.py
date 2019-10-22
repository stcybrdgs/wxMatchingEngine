#!/usr/bin/env python
# coding: utf8
"""
Mon, Oct 21, 2019
Stacy Bridges

This simplified code transforms an input set of brands into brand patterns
that can be used for string matching by the NERS EntityRuler.

"""
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

# identify i/o  --------------------------------------------------
outfile = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\out_brand_patterns.jsonl'
brands_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\in_brand.xlsx'
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
for brand in brands:
    # iterate thru brands
    # and build patterns using the pattern/token components from above
    brand = str(brand)  # eliminate any float objects
    char_count = 0
    is_last_char = False

    for char in brand:
        char_count += 1
        if char_count == len(brand):
            # set the flag if you've reached the last char in the brand string
            is_last_char = True

        if char in special_chars:
            if token != '':
                # if you reach a special char, then store the token that you've
                # built from the preceding chars
                tokens.append(token)
                token = ''
            if char == ' ':
                # if char is a space, make it empty so that spacy to use it
                char = ''
            # store the special char as a token
            tokens.append(char)
        else:
            token = token + char

        if is_last_char == True:
            tokens.append(token)
            token = ''

    # after iterating through the brand string, build the pattern from the
    # pattern/token components and the tokens that you've stored in the array
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

    # store the pattern in the pattern array
    pattern = pattern + ps
    patterns.append(pattern)

    # reset your pattern string and token array before parcing next brand string
    pattern = ''
    tokens.clear()

# write brand patterns to file  -------------------------------
# iterate through pattern array, writing each line to external file
# that can then be picked up by the EntityRuler to map Brands to the model
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
