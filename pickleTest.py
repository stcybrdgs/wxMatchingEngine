"""
Created on Sat Jun 15
@author: Stacy Bridges
"""
import pickle
import pickleTest_catch
# import sys


def make_pickle(d):
    f = "Emp.pickle"
    pickling_on = open(f,"wb")
    pickle.dump(d, pickling_on)
    pickling_on.close()
    return f

def open_pickle(f):
    pickle_off = open(f,"rb")
    emp = pickle.load(pickle_off)
    print('In open_pickle(): ', emp)

def main():
    emp = {1:"A",2:"B",3:"C",4:"D",5:"E"}
    print('In main(): ', emp)

    pickleFileName = make_pickle(emp)
    #open_pickle(pickleFileName)

    pickleTest_catch.catch_pickle(pickleFileName)



    print('Done.')

if __name__ == '__main__': main()
