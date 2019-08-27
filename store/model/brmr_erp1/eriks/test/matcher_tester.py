import spacy
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.matcher import PhraseMatcher
import re

"""
from spacy.matcher import PhraseMatcher

matcher = PhraseMatcher(nlp.vocab)
matcher.add("OBAMA", None, nlp(u"Barack Obama"))
doc = nlp(u"Barack Obama lifts America one last time in emotional farewell")
matches = matcher(doc)

# !!
# need to find ,{alpha} and replace with ,space{alpha}
# otherwise spacy can't see the pattern that may preceed the comma

----------------------

snippets:
{"label":"MPN", "pattern":[{"lower":"07342e-10"}]}
nu_ruler = EntityRuler(nlp).from_disk(patterns_file)
nlp.add_pipe(nu_ruler)#, before='ner')

ruler = EntityRuler(nlp)
ruler.add_patterns([{"label": "ORG", "pattern": "Apple"}])
nlp.add_pipe(ruler)

doc = nlp("A text about Apple.")
ents = [(ent.text, ent.label_) for ent in doc.ents]
assert ents == [("Apple", "ORG")]


ruler = EntityRuler(nlp)
ruler.add_patterns(patterns)

nlp = spacy.load("en_core_web_sm", disable=['ner'])
ruler = EntityRuler(nlp, overwrite_ents=True)
ruler.add_patterns(patterns)
nlp.add_pipe(ruler)

"""
# this method is fired only if a match is found upon matches = matcher(doc)
# this method is actually stored as a callback function within the matcher
# and is added when you add the pattern
def on_match(matcher, doc, id, matches):
    print('Matched!', matches)

# load model
nlp = spacy.load("en_core_web_sm")

# create matcher
matcher = Matcher(nlp.vocab)

# define patterns for the matcher
# rem regex can only be applied to attributes in TEXT, LOWER, TAG
rs_regex = r"^\d{3}[ -]\d{3,4}|[ ]\d{3}[ -]\d{3,4}"
mpn_patterns = [
    [{"TEXT": "6001"}],
    [{"TEXT": "6001"}, {"IS_PUNCT":True}, {"lower":"2rs"}],
    [{"TEXT": "6001"}, {"lower":"rs"}, {"lower":"c"}],
    [{"TEXT": "6001"}, {"lower":"2rs"}],
    [{"TEXT": {"REGEX": rs_regex}}],
    [{"TEXT": {"REGEX": r"^\d{3}"}}, {"IS_PUNCT":True}, {"TEXT": {"REGEX": r"^\d{3,4}"}}],
    [{"lower":"allen"},{"lower":"bradley"}],
    [{"lower":"stanley"},{"lower":"power"},{"lower":"tools"}],
    [{"TEXT": {"REGEX": "deff?in[ia]tely"}}]
]

# add patterns to the matcher
for item in mpn_patterns:
    matcher.add("MPNS", on_match, item)

# create nlp document
doc = nlp(u"Hello, world! Hello world! Hello-world, 6001 RS C, 6001, 6001-2RS, 6001 2RS, definitely Allen Bradley, and deffinitely Stanley Power Tools, or just Stanley, and 111-245 is an RS code, and so are 142-365 and 348-2901")

# find strings in nlp doc that match patterns in the matcher
matches = matcher(doc)

# for matches, print out info
for match_id, start, end in matches:
    #string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    #print(match_id, string_id, start, end, span.text)
    print(span.text)

'''
print('Match:', item)
#for i in item:
i = 0
for val in item:
    print(val)


print('sent.text, sent.pos_: ------------')
for sent in doc:
    print(sent.text, sent.pos_)

print('ent.text, ent.label_: ------------')
for ent in doc.ents:
    print(ent.text, ent.label_)
'''

print('Done.')
