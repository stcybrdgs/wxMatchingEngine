#!/usr/bin/env python
# coding: utf8
# model trainer test
# Compatible with: spaCy v2.0.0+

'''
Friday, July 12, 2019
Stacy Bridges
'''
import json

def update_meta():
    json_content = []
    nu_pipeline = ['tagger', 'ner', 'entity_ruler']

    # read in meta.json
    with open('model_entRuler/meta.json','r') as jsonfile:
        json_content = json.load(jsonfile)
        old_pipeline = json_content['pipeline']

    # update json_content to reflect new pipeline
    json_content['pipeline'] = nu_pipeline

    # write the new pipeline to the json file
    with open('model_entRuler/meta.json','w') as jsonfile:
        json.dump(json_content, jsonfile)

    # end function //
'''
def main():
    update_meta()

if __name__ == '__main__' : main()
'''
