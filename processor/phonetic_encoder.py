# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:49:44 2019
@author: Stacy

these scripts process strings per the phonetic encoding algorithms
included in the python jellyfish and doublemetaphone libraries.

rem
a combo of Soundex and Metaphone typically results in an
initial high number of positive matches

processor/
    phonetic_encoder.py
    # imports: [ sys, jellyfish, doublemetaphone ]
        def soundex(s)
        def metaphone(s)
        def double_metaphone(s)
        def nysiis(s)
        def match_rating_codex(s)

"""
# IMPORT LIBS  =====================================
import sys
import jellyfish
from metaphone import doublemetaphone

# FUNCTIONS  =======================================
'''
The Soundex algorithm converts a word (typically a name) to a
four digit code in the form ‘A123’ where ‘A’ is the first letter of
the name and the digits represent similar sounds
'''
def soundex(s):
    return jellyfish.soundex(s)
    # end function  //

'''
The Metaphone algorithm was designed as an improvement on Soundex.
It transforms a word into a string consisting of ‘0BFHJKLMNPRSTWXY’
where ‘0’ is pronounced ‘th’ and ‘X’ is a ‘[sc]h’ sound.
'''
def metaphone(s):
    return jellyfish.metaphone(s)
    # end function  //

'''
The Double Metaphone algorithm phonetically codes English words (and foreign
words often heard in the United States) by reducing them to a combination of
12 consonant sounds. It returns two codes if a word has two plausible
pronunciations, such as a foreign word. This reduces matching problems
that may occur due to incorrect spelling.
'''
def double_metaphone(s):
    return doublemetaphone(s)
    # end function  //

'''
The NYSIIS algorithm is an algorithm developed by the
New York State Identification and Intelligence System. It transforms a word
into a phonetic code. Like soundex and metaphone, it is primarily intended
for use on names (as they would be pronounced in English).
'''
def nysiis(s):
    return jellyfish.nysiis(s)
    # end function  //

'''
The Match Rating Approach algorithm is an algorithm for determining whether or
not two names are pronouncedsimilarly. The algorithm consists of an encoding
function that is similar to soundex or nysiis.
'''
def match_rating_codex(s):
    return jellyfish.match_rating_codex(s)
    # end function  //
