# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19
@author: Stacy Bridges

"""
# IMPORT LIBS  =====================================
import csv
import sys
import os
import re

# IMPORT PATHS  ====================================
sys.path.append('io/')
sys.path.append('ners/')
sys.path.append('preprocessor/')
sys.path.append('processor/')
sys.path.append('store/')

# IMPORT FUNCTIONS  ================================
import loader
import string_cleaner
import processor
import distanceEncoder

# GLOBALS  =========================================


# MAIN  ============================================
def main():
    f_txt = 'io/input/test/tender.txt'
    f_csv = 'io/input/test/tender.csv'

    d = loader.load_doc(f_csv)
    d = string_cleaner.clean_doc(d)

    # rem matcher:
    # if (distanceEncoder.levenshtein(d, d1)) == 0: 100% match

    # print to to console
    print('\n' + d)

    print('Done')

if __name__ == '__main__' : main()
