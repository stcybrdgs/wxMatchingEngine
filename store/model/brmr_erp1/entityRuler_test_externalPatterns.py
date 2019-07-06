#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
import spacy
#from spacy.lang.en import English
from spacy.pipeline import EntityRuler

def main():
    # load a language and invoke the entity ruler
    nlp = spacy.load('en_core_web_sm', disable=['parser']) #English()
    ruler = EntityRuler(nlp)

    # establish patterns for entity recognition
    patterns = [{"label": "ORG", "pattern": "Apple"},
                {"label": "GPE", "pattern": [{"lower": "san"}, {"lower": "francisco"}]},
                {"label": "SUPPLIER", "pattern": [{"lower": "fag"}]},
                {"label": "SUPPLIER", "pattern": [{"lower": "siemens"}]},
                {"label": "SUPPLIER", "pattern": [{"lower": "skf"}]},
                {"label": "PRODUCT", "pattern": [{"lower": "deep"}, {"lower": "groove"}, {"lower": "ball"}, {"lower": "bearing"}]},
                {"label": "PRODUCT", "pattern": [{"lower": "ball"}, {"lower": "bearing"}]},
                {"label": "PRODUCT", "pattern": [{"lower": "bearing"}]},
                #{"label": "MPN", "pattern": "6026-2RSRC3"},
                #{"label": "MPN", "pattern": [{"NUM":"6026"}, {"SYM":"-"}, {"NUM":"2RSRC3"}]}
               ]
    ruler.add_patterns(patterns)

    # putting the ruler before ner will override ner decisions in favor of ruler patterns
    nlp.add_pipe(ruler, before='ner')

    # show pipeline components:
    print(nlp.pipe_names)

    s1 = u"Apple has an office in San Francisco."
    s2 = u"I need a Deep Groove Ball Bearing by either FAG or skf, mpn 6026-2RSRC3."
    s3 = u"Also, a needle bearing by fag."
    s4 = u"A siemens brand needle ball bearing."
    sl = [s1, s2, s3, s4]
    sn = ""
    for item in sl:
        #for token
        sn = sn + item

    doc = nlp(sn)
    print([(ent.text, ent.label_) for ent in doc.ents])
    print([(token.text, token.pos_) for token in doc])

    # end program
    i = 0
    while i < 5:
        print('.')
        i += 1
    print('Done.')

if __name__ == '__main__' : main()
