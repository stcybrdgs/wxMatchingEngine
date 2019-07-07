#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
import spacy
#from spacy.lang.en import English
from spacy.pipeline import EntityRuler

def main():
    # load a language and invoke the entity ruler
    nlp = spacy.load('en_core_web_sm', disable=['parser']) #English()
    ruler = EntityRuler(nlp, overwrite_ents=True)

    # establish patterns for entity recognition
    # load from external file
    patterns = [{"label": "ORG", "pattern": "Apple"},
                {"label": "GPE", "pattern": [{"lower": "san"}, {"lower": "francisco"}]},
                {"label": "SUPPLIER", "pattern": [{"lower": "fag"}]},
                {"label": "SUPPLIER", "pattern": [{"lower": "siemens"}]},
                {"label": "SUPPLIER", "pattern": [{"lower": "skf"}]},
                {"label": "SUPPLIER", "pattern": [{"lower": "hill"}, {"lower":"pumps"}]},
                {"label": "SUPPLIER", "pattern": [{"lower": "excel"}, {"lower":"machine"},{"lower":"tools"}]},
                {"label": "PRODUCT", "pattern": [{"lower": "deep"}, {"lower": "groove"}, {"lower": "ball"}, {"lower": "bearing"}]},
                {"label": "SKU", "pattern": [{"lower":"wxw01941297"}]},
                {"label": "MPN", "pattern": [{"lower":"60262rsrc3"}]}
                #{"label": "PRODUCT", "pattern": [{"lower": "ball"}, {"lower": "bearing"}]},
                #{"label": "PRODUCT", "pattern": [{"lower": "bearing"}]}
                #{"label": "MPN", "pattern": [{"lower": "6026-2RSRC3"}]}
                #{"label": "MPN", "pattern": [{"NUM":"6026"}, {"SYM":"-"}, {"NUM":"2RSRC3"}]}
               ]
    ruler.add_patterns(patterns)

    ruler.to_disk('patterns2.jsonl')
    nu_ruler = EntityRuler(nlp).from_disk('patterns2.jsonl')
    # putting the ruler before ner will override ner decisions in favor of ruler patterns
    nlp.add_pipe(nu_ruler, before='ner')

    # show pipeline components:
    print(nlp.pipe_names)

    s1 = u"Apple has an office in San Francisco."
    s2 = u" I need a Deep Groove Ball Bearing by either FAG or skf with an mpn of 60262rsrc3."
    s3 = u" I also need a needle bearing by fag."
    s4 = u" A siemens brand needle ball bearing, sku is wxw01941297."
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
