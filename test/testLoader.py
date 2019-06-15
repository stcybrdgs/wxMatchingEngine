# -*- coding: utf-8 -*-
'''
Created on Fri Jun 14 2019
@author: Stacy Bridges
'''
# IMPORT  LIBS  ========================
#import json
import sys
import os

# PATHS ================================
# import importlib
# rem use importlib to import module stored as string
sys.path.append('../io/')
sys.path.append('../ners/')
sys.path.append('../processor/')
sys.path.append('../stores/')


# IMPORT FUNCTIONS  =====================
import loader
import preprocessor

# GLOBAL VARS  =========================

# LOCAL FUNCTIONS  =====================

# MAIN  ================================i
def main():
    # rem detect and load doc options
    #   from io/ :    mark
    #   from store/ : lookup, master, model, taxonomy
    '''# TEST LOADER
    # create an obj for the doc that is to be matched against the master
    matchDoc = loader.loadDoc('master')  #  ../processor/

    print(matchDoc)
    '''

    # TEST remove_special_chars(d)
    s = '22652|block    housing,     70mm high, 210 mm bolthole, 5.5 kg, from SKF|se509|1/2/2019|11|Ea|316.58'
    nuD = preprocessor.string_cleaner(s)
    print(nuD)

    # end program
    print('Done.')

if __name__ == '__main__' : main()
