"""
Wed Aug 21 2019
Stacy Bridges

# import unspsc commodity strings, appending each string to an array

# import tender file
# loop through each record to find a match in commodity strings
# if a match is found, print it to the pandas array and exit the loop
# print the pandas array

"""
import spacy
from spacy.matcher import Matcher
import sys


# PATHS  =======================================

# FUNCTIONS  ===================================
def sentence_segmenter(doc):
    for token in doc:
        if token.text == 'wrwx':
            doc[token.i].is_sent_start = True
    return doc
    # end function //

def main():
    # load model
    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(sentence_segmenter, after='tagger')
    matcher = Matcher(nlp.vocab)

    # Add match ID "HelloWorld" with no callback and one pattern
    pattern = [{"LOWER": "6001"}, {"IS_PUNCT": True}, {"LOWER": "RS"}]
    matcher.add("6001RS", None, pattern)

    print(nlp.pipe_names)

    doc = nlp(u"SKF Deep Groove Ball Bearing 6001,RS")
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)
        print('here')

    print('Done.')

if __name__ == '__main__': main()
