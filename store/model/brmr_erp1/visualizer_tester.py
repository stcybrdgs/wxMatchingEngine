#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
'''
Thursday, July 11, 2019
Stacy Bridges

Visualizer Tester

nlp = spacy.load("custom_ner_model")
doc = nlp(text)
displacy.serve(doc, style="ent")
'''
import spacy
from spacy import displacy

text = """But Google is starting from behind. The company made a late push
into hardware, and Apple’s Siri, available on iPhones, and Amazon’s Alexa
software, which runs on its Echo and Dot devices, have clear leads in
consumer adoption."""

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
displacy.serve([doc], style="ent", page = True, port = 80)


print('Done.')
