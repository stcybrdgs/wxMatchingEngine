#!/usr/bin/env python
# coding: utf8
# model trainer test
# Compatible with: spaCy v2.0.0+

'''
Saturday, July 13, 2019
Stacy Bridges

'''
# LIB IMPORTS =================================
import sys
import os
import spacy

# IMPORT PATHS ================================
sys.path.append('../../../preprocessor/')

# .PY IMPORTS =================================
import loader
#import string_cleaner

# GLOBALS  ====================================

# FUNCTIONS  ==================================

# training data
TRAIN_DATA = []
with open('train_data.txt') as data:
    i = 0
    for line in data:
        #row = line.rstrip()
        TRAIN_DATA.append(line)
        i += 1
print(TRAIN_DATA)
print('Done.')
