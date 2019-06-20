# -*- coding: utf-8 -*-
"""
Created on Tue Jun 4 16:57:36 2019
@author: Stacy Bridges

scripts to process strings per the distance encoding algorithms
included in the python jellyfish library.

processor/
    distance_encoder.py
    # imports: [ jellyfish ]
        def levenshtein(s1, s2)
        def damerau_levenshtein(s1, s2)
        def jaro(s1, s2)
        def jaro_winkler(s1, s2)
        def hamming(s1, s2)
        def match_rating_comparison(s1, s2)

"""
# IMPORT LIBS  =====================================
import jellyfish

# FUNCTIONS  =======================================
'''
Levenshtein distance represents the number of insertions,
deletions, and subsititutions required to change one word to
another.
'''
def levenshtein(s1, s2):
    return jellyfish.levenshtein_distance(s1, s2) # return one value
    # end function  //

'''
A modification of Levenshtein distance, Damerau-Levenshtein
distance counts transpositions (such as ifhs for fish) as
a single edit.
'''
def damerau_levenshtein(s1, s2):
    return jellyfish.damerau_levenshtein_distance(s1, s2) # return one value
    # end function  //

'''
Jaro distance is a string-edit distance that gives a floating
point response in [0,1] where 0 represents two completely
dissimilar strings and 1 represents identical strings.
'''
def jaro(s1, s2):
    return jellyfish.jaro_distance(s1, s2) # return one value
    # end function  //

'''
Jaro-Winkler is a modification/improvement to Jaro distance, like Jaro it
gives a floating point response in [0,1] where 0 represents two completely
dissimilar strings and 1 represents identical strings.
'''
def jaro_winkler(s1, s2):
    return jellyfish.jaro_winkler(s1, s2) # return one value
    # end function  //

'''
Hamming distance is the measure of the number of characters that
differ between two strings.
'''
def hamming(s1, s2):
    return jellyfish.hamming_distance(s1, s2) # return one value
    # end function  //

'''
Compare s1 and s2 using the match rating approach algorithm, returns True if
strings are considered equivalent or False if not. Can also return None if
s1 and s2 are not comparable (length differs by more than 3).

The Match rating approach algorithm is an algorithm for determining whether or
not two names are pronounced similarly. Strings are first encoded using
match_rating_codex() then compared according to the MRA algorithm.

MRA does not perform well with encoded names differing in length by more than 2.
'''
def match_rating_comparison(s1, s2):
    return jellyfish.match_rating_comparison(s1, s2) # return two values
    # end function  //
