# -*- coding: utf-8 -*-
'''
Created on Sat Jun 15 2019
@author: Stacy Bridges
'''
# IMPORT  LIBS  ========================
import sys
import os

# PATHS ================================
# import importlib
# rem use importlib to import module stored as string
sys.path.append('../io/')
sys.path.append('../ners/')
sys.path.append('../preprocessor/')
sys.path.append('../processor/')
sys.path.append('../store/')

# IMPORT FUNCTIONS  =====================
import loader
import preprocessor
import processor

# MAIN  =================================
def main():
    doc = loader.loadDoc('mark')
    print('get doc:\n ', doc)

    # clean the test string
    doc = preprocessor.string_cleaner(doc)
    print('\nstring clean doc:\n', doc)

    # create nlp object from test string
    processor.create_nlp_object(doc)


    # end program
    print('Done.')


if __name__=='__main__' : main()
