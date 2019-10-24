#!/usr/bin/env python
# coding: utf8
"""
Mon, Oct 21, 2019
Stacy Bridges

This simplified code transforms an input set of brands into brand patterns
that can be used for string matching by the NERS EntityRuler.

"""
# import library components  ---------------------------------------------------
import os, shutil, sys
import pathlib
from pathlib import Path
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

# import py files  -------------------------------------------------------------
import menu

def main():
    # print menu options to console  -----------------------------------------------
    # declare menu and file arrays
    menu_choices = []
    file_choices = []

    # get path of current folder
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # get names of .xlsx files that are in the folder that are also input files
    for r, d, f in os.walk(folder_path):  # rem r=root, d=dir, f=file
        for file in f:
            if '.xlsx' in file and 'brand' in file:
                # rem for full path use <files.append(os.path.join(r, file))>
                file_choices.append(file)

    # print user menu
    print('\n-----------------------------------------')
    print('           Brand Input Files')
    print('-----------------------------------------')
    spacer ='  '
    print('{}{}{}'.format('m', spacer, 'Show Main Menu'))
    menu_choices.append('m')
    i = 0
    for ic in file_choices:
        i += 1
        print('{}  {}'.format(i, ic))
        menu_choices.append(str(i))

    # get user input
    print('\nSelect an input file (or \'m\' for Main Menu)')
    gold_choice = input()

    # validate user input
    while gold_choice not in menu_choices:
        print('Invalid choice! Select an input file (or \'m\' for Main Menu)')
        gold_choice = input()

    if gold_choice == 'm':
        menu.main()

        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this program; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()

    # identify i/o  ----------------------------------------------------------------
    outfile_name = 'ners_brand_patterns.jsonl'
    outfile_path = folder_path + '\\' + outfile_name
    brands_file = folder_path + '\\' + file_choices[int(gold_choice)-1]
    brands_sheet = 'Sheet1'
    brands_data = pd.read_excel(brands_file, brands_sheet)
    brands = brands_data['BRAND']
    dataLabel = 'BRND'

    # declare variables  -----------------------------------------------------------
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

    # build brand patterns  --------------------------------------------------------
    print('\nBuilding brand patterns...\n')
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
                    # if char is a space, make it empty so that spacy lib can use it
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

    # write brand patterns to file  ------------------------------------------------
    # iterate through pattern array, writing each line to external file
    # that can then be picked up by the EntityRuler to map Brands to the model
    brand_count = 0
    with open(outfile_path, 'w') as outfile:
        for line in patterns:
            outfile.write(line)
            outfile.write('\n')
            print(line)
            brand_count += 1

    # end program
    print('\n')
    print('Done.')
    print('{} brand patterns written'.format(brand_count))
    print('{}'.format(outfile_path))

if __name__ == '__main__' : main()
