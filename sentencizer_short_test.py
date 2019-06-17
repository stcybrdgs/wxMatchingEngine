# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17
@author: Stacy Bridges

test specifying terminal chars for the sentencizer

"""

# IMPORT LIBS  ======================================
import spacy
from spacy.lang.en import English
#from spacy.lang.en.examples import sentences

# IMPORT FUNCTIONS  =====================

# FUNCTIONS  =======================================

def main():
    # get just the language with no model
    #nlp = English()

    # get english language model
    nlp = spacy.load('en_core_web_sm')

    # add the sentencizer component to the pipeline
    # rem this component  splits sentences on punctuation such as . !  ?
    # plugging it into pipeline to get just the sentence boundaries
    # without the dependency parse.
    #sentencizer = nlp.create_pipe("sentencizer")
    #nlp.add_pipe(sentencizer)


    # TEST print  -----------------------
    # print('\n', nlp.pipeline)
    # print('\n', nlp.pipe_names)

if __name__ == '__main__' : main()
