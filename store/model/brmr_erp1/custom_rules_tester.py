#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
'''
Thursday, July 11, 2019
Stacy Bridges

Lemmatizer Tester

'''
# IMPORTS  -----------------------------
import spacy
import sys
import os
from spacy.matcher import Matcher
from spacy.tokens import Span

# IMPORT PATHS  ====================================
sys.path.append('../../../preprocessor/')

# IMPORT FUNCTIONS  ================================
import string_cleaner

# GLOBALS  =========================================
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

# FUNCTIONS  =======================================
def found_pattern(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    entity = Span(doc, start, end, label="EVENT")
    doc.ents += (entity,)
    print(entity.text)

def apply_custom_rules(d):

    str_doc = ''


    pattern = [{"IS_DIGIT": True}, {"ORTH": "-"}, {"IS_DIGIT": True}]
    matcher.add("Num_Hyph_Num", found_pattern, pattern)
    doc = nlp(d)
    matches = matcher(doc)

    # hyphens to colons ----------------------------
    # replace 12-123 pattern with 12:123
    # rem   pos_ of 12-123 returns NUM SYM NUM but
    #       pos_ of 12:123 returns NUM

    #for tok in doc:

    # commas to whitespace if not numerical --------
    # rem replace '1,000, token' with '1,000 token'
    #   stuff goes here
    return str_doc
    # end function //

# MAIN  ============================================
def main():
    # create nlp doc
    #start_string = '50123, 50 FAG ball bearings with a SKU of [523-421] and a MPN of 1234:1'
    start_string = '523-421 and 1234:1 and AB-23 and 23-AB and AB-21-AC-23'
    #doc = nlp(start_string)

    nu_start_string = apply_custom_rules(start_string)

    print(start_string)
    print(nu_start_string)

    '''
    # test string cleaner in preprocessor
    fin_str_doc = string_cleaner.clean_doc(start_string)
    print('\n{}'.format(start_string))
    print (fin_str_doc)
    '''

    # end program
    print('\nDone.')


if __name__ == '__main__' : main()
