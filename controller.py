# -*- coding: utf-8 -*-
'''
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
    
stemmer.py
    def porterStemmer()
    
    
'''
# IMPORTS  =============================
# sys path
import json
import sys
sys.path.append('matcher/')

# py files
import phoneticEncoder
import distanceEncoder

# GLOBALS  =============================


# MAIN  ================================
def main():
    # menu:
    # read and parse json file of modules and methods into console menu
    print('\n----------------------  MENU  ----------------------')
    print('m  -  menu\ne  -  exit')
    
    # create arrays to contain menu information
    # so that correct method is triggered when user makes a menu choice
    menuNumber = []  # array to contain menu numbers
    menuMethod = []  # array to contain methods that go with each menu number
    
    j = 0
    txt = ' - '
    with open('modulesMethods.json') as json_file:
        data = json.load(json_file)
        
        # print out the module name and a menu number
        for m in data['modules']:
            print('\n')
            print(m['module'] + ':')
            i = 0
            
            # print out the method name
            for f in m['methods']:
                if j >= 10: txt = '- '
                print(j, txt, m['methods'][i])
                # push method name and menu number to array
                menuNumber.append(j) 
                menuMethod.append(m['methods'][i]) 
                j += 1
                i += 1
    json_file.close()
    
    print('\n')
    print('----------------------------------------------------')       

    '''
    # TEST menu arrays
    print('menuNumber array: ')
    i = 0
    for item in menuNumber:
        print(i, ' - ', menuMethod[i])
        i += 1
    print('\n')
    
    '''
    # declare strings to pass to methods
    s1 = 'Jellyfish'
    s2 = 'Smellyfish'
    
    # get menu selection from user
    choice = input('Select a menu item: ')
    
    # process the user's menu selection
    while choice != 'e':
        # catch invalid user selection
        match = False
        for i in menuItems:
            if i == choice: match = True
        if match == False: print('Invalid selection.')
        
        # process valid user selection
        else:
            if choice == 'e': break # end program
            if choice == 'm': menu()
            if choice == '1': spacy_modules.tokenizer()
            if choice == '2': spacy_modules.tagger()
            if choice == '3': spacy_modules.parser()
            if choice == '4': spacy_modules.ner()
            if choice == '5': spacy_modules.matcher()
            if choice == '6': jf_phoneme.soundex()
            if choice == '7': jf_phoneme.nysiis()
            if choice == '7b': dm_doubleMetaphone.dlbMetaphone()
            if choice == '8': jf_distance.levenshtein()
            if choice == '9': jf_distance.jaroWinkler()
            if choice == '0': jf_match.mrc()
        
        # get new user selection
        choice = input('\nSelect a menu item: ')
        
    # end program
    print('Done.')

if __name__ == '__main__' : main()