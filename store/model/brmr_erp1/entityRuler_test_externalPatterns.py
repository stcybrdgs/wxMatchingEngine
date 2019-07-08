#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+

# IMPORTS  =====================================
import spacy
from spacy.pipeline import EntityRuler
#from spacy.lang.en import English

# FUNCTIONS  ===================================
def import_csv(d):
    global row_heads
    doc = ''
    with open(d) as data:
        csv_reader = csv.reader(data, delimiter='|')
        i = 0
        for row in csv_reader:
            # populate row_heads[]
            #if i > 0:  # skip header row
            row_head = row[0]
            row_heads.append(row_head)
            # populate txt obj
            doc = doc + ('|'.join(row) + '\n')
            i += 1
    return doc
    # end function //

# MAIN  ========================================
def main():
    # load a language and invoke the entity ruler
    nlp = spacy.load('en_core_web_sm', disable=['parser']) #English()

    # load patterns from external file
    # first, combine external files into a single file
    mpn = open('ners_patterns_mpn.jsonl', 'rt')
    sku = open('ners_patterns_sku.jsonl', 'rt')
    sup = open('ners_patterns_supplier.jsonl', 'rt')
    prod = open('ners_patterns_product.jsonl', 'rt')
    all = open('ners_patterns_all.jsonl', 'wt')
    for line in mpn:
        all.writelines(line)
        print('', end='', flush=True) # rem flush the output buffer
    for line in sku:
        all.writelines(line)
        print('', end='', flush=True) # rem flush the output buffer
    for line in sup:
        all.writelines(line)
        print('', end='', flush=True) # rem flush the output buffer
    for line in prod:
        all.writelines(line)
        print('', end='', flush=True) # rem flush the output buffer
    mpn.close()
    sku.close()
    sup.close()
    prod.close()
    all.close()

    nu_ruler = EntityRuler(nlp).from_disk('ners_patterns_all.jsonl')
    #nu_ruler2 = EntityRuler(nlp).from_disk('ners_patterns_supplier.jsonl')

    # putting the ruler before ner will override ner decisions in favor of ruler patterns
    nlp.add_pipe(nu_ruler, before='ner')
    #nlp.add_pipe(nu_ruler2, before='ner')

    # show pipeline components:
    print(nlp.pipe_names)

    with open('brammer_tender_temp.txt', 'r') as tender:

    s1 = u"Apple has an office in San Francisco."
    s2 = u" I need a (deep groove ball bearing) by either FAG or skf with an mpn of 60262rsrc3."
    s3 = u" I also need a needle bearing by fag, a spare tube,  and a plastic blow gun."
    s4 = u" I need a dirty water pump, a ball bearing, and a siemens brand needle roller bearing, sku is wxw01941297."
    s5 = u" tool apron, stanley Tools."
    sl = [s1, s2, s3, s4, s5]
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
