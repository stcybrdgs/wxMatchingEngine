# -*- coding: utf-8 -*-
'''
Created on Fri Jun 14 2019
@author: Stacy Bridges
'''

# IMPORTS  =============================
#import json
import sys
import os
import loader

# PATHS ================================
#import importlib  # use importlib to import module stored as string
#sys.path.append('../ners/')
sys.path.append('../processor/')
#sys.path.append('../stores/')
#sys.path.append('C:/Users/Owner/Anaconda3/Lib/site-packages') # jellyfish path
#sys.path.append('test/')
sys.path.append('../io/')

# GLOBALS  =============================


# LOCAL FUNCTIONS  =====================


# MAIN  ================================
def main():
    inFile = loadDoc('match')
    print(inFile)

    # end program
    print('Done.')

if __name__ == '__main__' : main()
