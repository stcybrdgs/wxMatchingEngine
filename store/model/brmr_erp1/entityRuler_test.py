#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
from spacy.lang.en import English
from spacy.pipeline import EntityRuler

# load a language and invoke entity ruler
nlp = English()
ruler = EntityRuler(nlp)

# establish patterns for entity recognition
patterns = [{"label": "ORG", "pattern": "Apple"},
            {"label": "GPE", "pattern": [{"lower": "san"}, {"lower": "francisco"}]},
            {"label": "SUPPLIER", "pattern": [{"lower": "fag"}]},
            {"label": "SUPPLIER", "pattern": [{"lower": "skf"}]},
            {"label": "PRODUCT", "pattern": [{"lower": "deep"}, {"lower": "groove"}, {"lower": "ball"}, {"lower": "bearing"}]},
            {"label": "PRODUCT", "pattern": [{"lower": "ball"}, {"lower": "bearing"}]},
            {"label": "PRODUCT", "pattern": [{"lower": "bearing"}]},
            {"label": "MPN", "pattern": "6026-2RSRC3"}
           ]
ruler.add_patterns(patterns)
nlp.add_pipe(ruler)

# show pipeline components:
print(nlp.pipe_names)

doc = nlp(u"Apple has an office in San Francisco. I need a Deep Groove Ball Bearing by either FAG or SKF, mpn 6026-2RSRC3. Also, a needle bearing by fag.")
print([(ent.text, ent.label_) for ent in doc.ents])
print([(token.text) for token in doc])
