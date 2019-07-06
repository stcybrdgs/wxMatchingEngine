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
pattern_1 = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
pattern_2 = [{"LOWER": "hello"}, {"LOWER": "world"}]

matcher.add("HelloWorld", None, pattern_1, pattern_2)

doc = nlp(u"Hello, world! Hello! Hello world! Hello, there, world!")
matches = matcher(doc)
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    print(match_id, string_id, start, end, span.text)


# by default, the matcher only returns matches and nothing else.
# if you want it to merge entities, assign labels, or something else,
# then you can define such actions for each pattern by passing in a
# callback function as the on_match argument on add(), ie:
# matcher.add("StringID", myCallBack, pattern)
