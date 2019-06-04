# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:49:44 2019
@author: Stacy

Phonetic Encoding Modules
    dblMet  -  	Double Metaphone
    jf -        Metaphone
    jf - 		Soundex				        sounds like	*
    jf - 		Metaphone			        sounds like	*
    jf - 		NYSIIS				        sounds like
    jf - 		Match Rating Approach Codex 
    tbd - 		Phonex				        sounds like	*

    * rem: 
    LIG algorithms combine index of similarity with Phones 
    (combo of Soundex and Metaphone) and resultin an initial high 
    number of positive matches    
    
"""
import jellyfish
from metaphone import doublemetaphone

'''
Soundex is an algorithm to convert a word (typically a name) to a 
four digit code in the form ‘A123’ where ‘A’ is the first letter of 
the name and the digits represent similar sounds
'''
def soundex(s):
    print('Running Soundex...')
    
    # end function  -----------

'''    
The metaphone algorithm was designed as an improvement on Soundex. 
It transforms a word into a string consisting of ‘0BFHJKLMNPRSTWXY’ 
where ‘0’ is pronounced ‘th’ and ‘X’ is a ‘[sc]h’ sound.
'''
def metaphone(s):
    return metaphone(s)
    # end function  -----------
    
def doubleMetaphone(s):
    return doublemetaphone(s)
    
    # end function  -----------
    
def nysiis(s):
    print('Running NYSIIS...')
    
    # end function  -----------
    
def matchRatingCodex(s):
    print('Running Match Rating Codex...')
    
    # end function  -----------
    
def phonex(s):
    print('Running Phonex...')
    
    # end function  -----------
    

