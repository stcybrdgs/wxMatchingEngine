# -*- coding: utf-8 -*-
'''
Created on Wed Jun  5 16:39:57 2019
@author: Stacy Bridges

'''
# IMPORTS  =========================================
import jellyfish

# FUNCTIONS  =======================================
'''
Reduce the string s to its stem using the common Porter stemmer.
Stemming is the process of reducing a word to its root form, for example ‘stemmed’ to ‘stem’.
Martin Porter’s algorithm is a common algorithm used for stemming that works for many purposes.
'''
def porterStemmer(s):
    # print('Porter Stemmer...')
    return jellyfish.porter_stem(s)

    # end function