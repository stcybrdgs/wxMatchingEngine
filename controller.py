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
import json
import sys
sys.path.append('matcher/')

# py files
import phoneticEncoder
import distanceEncoder

# GLOBALS  =============================


# MAIN  ================================
def main():
    # read and parse json file of modules and methods
    with open('modulesMethods.json') as json_file:
        data = json.load(json_file)
        print(data)
        
        for m in data['modules']:
            print('Module: ' + m['module'])
            i = 0
            for f in m['methods']:
                print('Methods: ', m['methods'][i])
                i += 1

    # __________________________________________________________ ADD MENU BEG
    # USE THIS SECTION TO ADD MODULES AND METHODS 
    # THE MENU
    
    # declare list of modules
    modules = ['Phonetic Encoder', 'Distance Encoder']  
    
    # declare lists of methods that are in each module 
    methods_0 = ['Soundex', 'Metaphone', 'Double Metaphone', 
                 'NYSIIS', 'Match Rating Codex']  
    methods_1 = ['Levenshtein Distance', 'Damerau Levenshtein Distance', 
                 'Jaro Distance', 'Jaro-Winkler Distance', 
                 'Hamming Distance', 'MatchRatingComparison']

    # declare lists of methods for each module 
    # (module[0] goes with methods_0, module[1] goes with methods_1, etc)
    methods = [methods_0, methods_1] 
    
    # __________________________________________________________ ADD MENU END
    
    
    # print the menu to the console
    print('\n----------------------  MENU  ----------------------')
    print('m  -  menu\ne -  exit\n')
    i = 0; j = 0; txt = ' - '  # sentinels
    for module in modules:
        print(module, ':')
        for method in methods[i]:
            if j >= 10: txt = '- '
            print(j, txt, method)
            j += 1
        i += 1
        print('\n')
    print('----------------------------------------------------')    
    
    
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