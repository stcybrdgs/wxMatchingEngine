# -*- coding: utf-8 -*-
'''
Created on Tue Jun  4 15:11:52 2019
@author: Stacy Bridges

processor/
    phoneticEncoder.py
        def soundex(s)
        def metaphone(s)
        def doubleMetaphone(s)
        def nysiis(s)
        def matchRatingCodex(s)
    
    distanceEncoder.py
        def levenshtein(s1, s2)
        def damerauLevenshtein(s1, s2)
        def jaro(s1, s2)
        def jaroWinkler(s1, s2)
        def hamming(s1, s2)
        def matchRatingComparison(s1, s2)
 
preProcessor/
    stringCleaner.py
        def porterStemmer(s)
    
'''
# IMPORTS  =============================
# sys path
import json
import sys
import importlib  # use importlib to import module stored as string
sys.path.append('processor/')
sys.path.append('preProcessor/')

# py files
import phoneticEncoder
import distanceEncoder
import stringCleaner


# GLOBALS  =============================
# create arrays to contain menu information so that
# the correct method is triggered when user makes a menu choice
menuNumbers = []  # array to contain menu numbers
menuMethods = []  # array to contain methods that go with each menu number
methodDefs = [] # array to contain the defs that go with each menu number

# declare test strings to pass to methods
s = "belly wish"
s1 = "jelly fish"
s2 = "deli fish"


# LOCAL FUNCTIONS  =====================
def menu():
    # read and parse json file of modules and methods into console menu
    print('\n----------------------  MENU  ----------------------')
    print('m  -  menu\ne  -  exit')
    
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
                menuNumbers.append(j) 
                menuMethods.append(m['methods'][i]) 
                methodDefs.append(m['methodDefs'][i])
                j += 1
                i += 1
    json_file.close()
    
    print('\n')
    print('----------------------------------------------------')    

def getModuleDef(string):
    moduleDef = "empty"
    with open('modulesMethods.json') as json_file:
        data = json.load(json_file)
        
        # find module based on string (ie, the module where the
        # user's selected method is located)
        for m in data['modules']:
            # print out the method name
            for f in m['methodDefs']:
                if string == f:
                    print('method: {}, methodDef: {}, module: {}'.format(string, f, m['moduleDef']))
                    moduleDef = m['moduleDef']
    json_file.close()
    return moduleDef
    
def callMethod(string):
    '''
    # template to run function stored as string:
    import amodule 
    varstring = 'f'  # 'f' is function by amodule.py import
    function = getattr(amodule,varstring) 
    function()
    '''
    # call function with 2 args if 's1' is found in methodName, else
    # call function with 1 arg
    methodString = ""
    locof1 = string.find('1')
    locofpar = string.find('(')
    numArgs = 0
    if locof1 < 1: 
        numArgs = 1 
        methodString = string[0:locofpar]
    else: 
        numArgs = 2
        methodString = string[0:locof1-2]

    moduleDef = getModuleDef(string)
    # use importlib to import the correct module that was 
    # stored as a string
    importModule = importlib.import_module(moduleDef)
    function = getattr(importModule, methodString)
    if numArgs == 1: 
        print('Input string(s): {}'.format(s))
        return function(s)
    else: 
        print('Input string(s): {}, {}'.format(s1, s2))
        return function(s1, s2) 
    

    
# MAIN  ================================
def main():
    # print test menu to console
    menu()      
    # testCount = 0
    # get and process the user's menu selection
    choice = input('Select a menu item: ')
    result = ''
    while choice != 'e':
        match = False
        methodName = ''
        
        # catch invalid user selection
        for i in menuNumbers:
            if choice == str(menuNumbers[i]): 
                match = True
                methodName = methodDefs[i]
        if choice == 'e': break # end program
        elif choice == 'm':  menu()
        elif match != True:
            print('You selection is not valid.')
        else:
            # call method that was selected by the user
            result = callMethod(methodName)
            print('Result: ', result)
        choice = input('Select a menu item: ')
       
    # end program
    print('Done.')

if __name__ == '__main__' : main()