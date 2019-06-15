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
    ts = ' 88325| Plummer housing by SKF with 2100  (mm) bolt hole and 700 (mm) in   height|se511609k7 ? (not sure, ask Enrìque Lòpez)'
    ts2 = '18132| Örsted Müller asked for the needle  bearing set by   NKX, 110 MM bolt-hole centr distance, height 30 mm, weight 1.83 kg|NKX 15z? (not sure)'
    print(ts)

    # clean the test string
    ts = preprocessor.string_cleaner(ts)
    print(ts)

    # create nlp object from test string
    processor.create_nlp_object(ts)

    # end program
    print('Done.')


if __name__=='__main__' : main()
