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
    s = ' 88325| Plummer housing by SKF with 2100  (mm) bolt hole and 700 (mm) in   height|se511609k7 ? (not sure, ask Enrìque Lòpez)\n18132| Örsted Müller asked for the needle  bearing set by   NKX, 110 MM bolt-hole centr distance, height 30 mm, weight 1.83 kg|NKX 15z? (not sure)'
    print(s)
    nuD = preprocessor.string_cleaner(s)
    print(nuD)


    # end program
    print('Done.')

if __name__ == '__main__' : main()
