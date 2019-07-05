# -*- coding: utf-8 -*-
'''
Created July 5 2019
Stacy Bridges

spaCy features a rule-matching engine, the Matcher, that operates over tokens,
similar to regular expressions. The rules can refer to token annotations
(e.g. the token text or tag_, and flags (e.g. IS_PUNCT). The rule matcher also
lets you pass in a custom callback to act on matches – for example, to merge
entities and apply custom labels. You can also associate patterns with entity IDs,
to allow some basic entity linking or disambiguation. To match large terminology
lists, you can use the PhraseMatcher, which accepts Doc objects as match patterns.

'''
import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')

# initialize Matcher with a vocab
# rem Matcher must share vocab with documents
#     it operates upon
matcher = Matcher(nlp.vocab)

# call matcher.add with no callback and one custom pattern
# (if you use a callback, it is invoked on a successful match)
# rem each dictionary represents one token
pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
matcher.add("HelloWorld", None, pattern)

doc = nlp(u"Hello, world! Hello world!")
matches = matcher(doc)
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    print(match_id, string_id, start, end, span.text)
