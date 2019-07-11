#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
'''
Thursday, July 11, 2019
Stacy Bridges

Visualizer Tester

'''
import spacy
import sys
import os
from spacy import displacy
import os
sys.path.append('../../../preprocessor/')
import loader

infile = 'iesa_tender.csv'
nlp = spacy.load("en_core_web_sm")
doc = nlp(loader.load_doc(infile))


html = displacy.render(doc, style="ent", page=True)

with open('C:/xampp/htdocs/mySites/wrWx_NERS/index.html', 'w') as data:
    data.write(html)

print(html)


print('Done.')
