import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

# test data  -----------------------------------------------
'''
brands = ['3M','A & A','A K FLUIDTECH','AAF',
    'AAK BALERY','ACCU-CODER','PEPPERL&FUCHS',
    'PEPPERL & FUCHS','PEPPERL+FUCHS','PEPPERL + FUCHS'
]
'''
brands_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\in_brnd.xlsx'
brands_sheet = 'in_brnd'
brands_data = pd.read_excel(brands_file, brands_sheet)
brands = brands_data['BRAND']
dataLabel = 'BRND'

# declare variables  --------------------------------------
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

# build patterns  ------------------------------------------
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
            pass

    # test  ---------------------------
    print(tokens)
    tokens.clear()

# end program
print('Done.')
