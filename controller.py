# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:11:52 2019
@author: Stacy Bridges

phoneticEncoder.py
    def soundex(s)
    def metaphone(s)
    def doubleMetaphone(s)
    def nysiis(s)
    def matchRatingCodex(s)
    
distanceEncoder.py
    def levenshtein()
    def damerauLevenshtein()
    def jaro()
    def jaroWinkler()
    def hamming()
    def matchRatingComparison()
    
"""
# IMPORTS  =============================
# sys path
import sys
sys.path.append('matcher/')

# py files
import phoneticEncoder
import distanceEncoder

# GLOBALS  =============================

# LOCAL FUNCTIONS  =====================
def menu():
    # declare menu selections for each module
    modules = ['Phonetic Encoder', 'Distance Encoder']
    
    # declare methods for each module
    # the phonetic encoder
    methods_0 = ['Soundex', 'Metaphone', 'Double Metaphone', 'NYSIIS', 'Match Rating Codex']
    
    # the distance encoder
    methods_1 = ['Levenshtein Distance', 'Damerau Levenshtein Distance', 'Jaro Distance', 'Jaro-Winkler Distance', 'Hamming Distance']
    
    # print menu to console
    print('\n')
    print('----------------------  MENU  ----------------------')
    print('m  -  menu')
    print('e -  exit')
    
    methodNum = 0
    methodName = 'methods_' + str(methodNum)
    menuItem = 0
    for module in modules:
        print('\n', mod, ':')
            for method in methodName:
                print('  ', menuItem, ' - ', methodName[method])
                menuItem += 1

    # print('\n')
    print('----------------------------------------------------')
    # ----  end function  ----
    
# MAIN  ================================
def main():
    # stuff goes here
    
    # end program
    print('Done.')

if __name__ == '__main__' : main()