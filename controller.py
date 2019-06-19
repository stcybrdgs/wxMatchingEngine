# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19
@author: Stacy Bridges

"""
# IMPORT LIBS  =========================
import csv
import sys
import os
import re

# PATHS  ===============================
sys.path.append('io/')
sys.path.append('ners/')
sys.path.append('preprocessor/')
sys.path.append('processor/')
sys.path.append('store/')

# FUNCTIONS  ===========================
import loader
import preprocessor
import processor

# GLOBALS  =============================


# MAIN  ================================
def main():
    f_txt = 'io/input/test/tender.txt'
    f_csv = 'io/input/test/tender.csv'

    d = loader.load_doc(f_csv)

    # print to to console
    print(d)

    print('Done')

if __name__ == '__main__' : main()
