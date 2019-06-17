# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17
@author: Stacy Bridges

test specifying terminal chars for the sentencizer

"""

# IMPORT LIBS  ======================================
import spacy
import sys
import os
#import spacy
#from spacy.lang.en import English
# from spacy.lang.en.examples import sentences

# PATHS ================================
sys.path.append('../preprocessor/')

# IMPORT FUNCTIONS  =====================
import preprocessor


# CUSTOM PIPES  =========================
def custom_sentencizer(doc):
    for i, token in enumerate(doc[:-2]):
        # Define sentence start if pipe + titlecase token
        if token.text == "|" and doc[i+1].is_title:
            doc[i+1].is_sent_start = True
        else:
            # Explicitly set sentence start to False otherwise, to tell
            # the parser to leave those tokens alone
            doc[i+1].is_sent_start = False
    return doc

def common_key_tagger(doc):
    print("After tokenization, this doc has {} tokens.".format(len(doc)))
    print("The part-of-speech tags are:", [token.pos_ for token in doc])
    if len(doc) < 10:
        print("This is a pretty short document.")
    return doc

# MAIN  =======================================
def main():
    # get just the language with no model
    #nlp = English()

    # get english language model
    nlp = spacy.load('en_core_web_sm', disable=['parser'])

    # add pipeline components
    nlp.add_pipe(custom_sentencizer, before="ner")  # Insert before the parser
    nlp.add_pipe(common_key_tagger, name="common_key_tagger", last=True)

    print(nlp.pipe_names)

    # lu adding: entity_ruler, merge_noun_chunks
    # https://spacy.io/usage/processing-pipelines/

    # add the sentencizer component to the pipeline
    # rem this component  splits sentences on punctuation such as . !  ?
    # plugging it into pipeline to get just the sentence boundaries
    # without the dependency parse.
    #sentencizer = nlp.create_pipe("sentencizer")
    #nlp.add_pipe(sentencizer)

    s1 = '155A8267|Internal Gear Pump|PARKER HANNIFIN|3339111325|Direction of Rotation Clockwise (CW), Flange Mounting 98.4x18.2 - �50.77 rectangular, Maximum Working Pressure (Bar) 120, Max Speed (RPM) 100, Pump Displacement (cc per rev) 170| �87.39'
    s2 = '155A8292|Internal Gear Pump|PARKER HANNIFIN|339111329|Direction of Rotation Clockwise (CW), Flange Mounting 98.4x128.2 - �50.77 rectangular, Maximum Working Pressure (Bar) 160, Max Speed (RPM) 2400, Pump Displacement (cc per rev) 70| �35.64'

    st1 = preprocessor.string_cleaner(s1)
    st2 = preprocessor.string_cleaner(s2)

    print(st1)
    print(st2)

    print('\n\n')

    row1 = nlp(st1)
    row2 = nlp(st2)
    print(row1.text)
    print(row2.text)





    # TEST print  -----------------------
    # print('\n', nlp.pipeline)
    # print('\n', nlp.pipe_names)

if __name__ == '__main__' : main()
