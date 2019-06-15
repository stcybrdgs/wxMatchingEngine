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

# GLOBAL VARS  =========================

# LOCAL FUNCTIONS  =====================

# MAIN  ================================i
def main():
    # rem detect and load doc options
    #   from io/ :    match
    #   from store/ : lookup, match, master, model , pickle , taxonomy

    # create an obj for the doc that is to be matched against the master
    matchDoc = loader.loadDoc('match')  #  ../processor/

    print(matchDoc)


    # end program
    print('Done.')

if __name__ == '__main__' : main()
