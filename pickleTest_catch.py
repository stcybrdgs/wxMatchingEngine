"""
Created on Sat Jun 15
@author: Stacy Bridges
"""
import pickle

def catch_pickle(f):

    pickle_off = open(f,"rb")
    emp = pickle.load(pickle_off)
    print('In catch_pickle(): ', f, emp)
