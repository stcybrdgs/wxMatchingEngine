#!/usr/bin/env python
# coding: utf8
# model trainer test
# Compatible with: spaCy v2.0.0+

'''
Friday, July 5, 2019
Stacy Bridges

Step by step guide (per spaCy documentation):
1.  Load the model you want to use (erp data set).
    If it is an existing model, use nlp.disable_pipes to disable all pipes but NER.
2.  Shuffle and loop over your examples (suppliers & products).
    For each example, use nlp.update to update the model.
    The updater will step through the words of the input. At each word, it will
    make a prediction and then consult the annotations to see if it is correct.
    If not, it will adjust weights to make the correct action score higher next time.
3.  Save the trained model using nlp.to_disk.
4.  Test the model to make sure the entities in the training data are recognized correctly.

For more details, see the documentation:
-   Training: https://spacy.io/usage/training
-   NER: https://spacy.io/usage/linguistic-features#named-entities

# brmr training data:
("93345|FESTO cylinder 63-80-PPVA-N3 sku: PKU-10003511|9/23/18|6|ea|181.02",{"entities": [(47-7, 59-7, "SKU")]}),
("00-3-A-F|SEW GEARBOX 60/1400RPM SEW SA57/T AD2 SA57/T AD2|P74-MOT-02186|SEW|SA57/T AD2",{"entities": [(65-7, 78-7,"SKU"),(83-7, 93-7, "MPN")]}),
("FAG DEEP GROOVE BALL BEARING 6026-2RSRC3", {"entities": [(0, 3, "SUPPLIER"), (4, 28, "PRODUCT"), (29, 40, "MPN")]}),
("19724|meyn lamp vision grading pll 55w/84 89.4140.904.0282|12/15/18|11|ft|342.43",{"entities": [(18-7, 22-7, "PRODUCT")]}),
("22652|AFC large size o-ring|1/2/19|11|Ea|316.58",{"entities": [(28-7, 34-7, "PRODUCT")]}),
("25027|schneider relay ca2 dn31 f7 telemec cad32f7|1/21/19|16|Pack|1515.84",{"entities": [(23-7, 28-7, "PRODUCT")]}),
("80442|OMRON RELAY 24VAC DPCO MK|3/22/19|18|Ea|4.48",{"entities": [(19-7, 24-7, "PRODUCT")]}),
("36199|HARTING SAFE EDGE CONNECTOR MALE R033|R033|8/8/18|1|Ea|341.8",{"entities": [(21-7, 45-7, "PRODUCT")]}),
("25027|skf bearing 6216-2rs 6216-2rs1:skf|1/21/19|16|Pack|1515.84",{"entities": [(17-7, 24-7, "PRODUCT")]}),
("55952|Push button greeng arrow by Reiser (Rieser ?)|11/18/18|16|Ea|1274.24",{"entities": [(13-7, 24-7, "PRODUCT")]}),
("19720|Siemens brand auxilary contactor |12/15/18|11|ft|342.43",{"entities": [(27-7, 45-7, "PRODUCT")]}),
("19724|Another Bussman fuse, 2amp w/antisurge feature|12/15/18|11|ft|342.43",{"entities": [(29-7, 33-7, "PRODUCT")]}),
("93345|FESTO cylinder 63-80-PPVA-N3 |9/23/18|6|ea|181.02",{"entities": [(19-7, 27-7, "PRODUCT")]}),
("70863|I need one Gas Strut engineering gas Strut,  . 3075aa-200n|3075AA-200N|8/31/18|1|each|31.75",{"entities": [(34-7, 55-7, "PRODUCT")]}),
("88325|stanley wrench adjustable 150mm lg roebuck|3/1/19|14|ft|745.78",{"entities": [(21-7, 27-7, "PRODUCT")]}),
("22652|A lmi repair kit for a dosing pump in eff plant (sp-u6)|1/2/19|11|Ea|316.58",{"entities": [(19-7, 29-7, "PRODUCT")]}),
("bearing fag  60032rsr",{"entities": [(20-7, 28-7, "MMAT")]}),
("bearing 6202c2z",{"entities": [(15-7, 22-7, "MMAT")]}),
("bearing fag  6204c2z",{"entities": [(20-7, 27-7, "MMAT")]}),
("bearing fag  62012rsr",{"entities": [(20-7, 28-7, "MMAT")]}),
("bearing fag  60022rsr",{"entities": [(20-7, 28-7, "MMAT")]}),
("bearing ball race 2307tvhc3 fag  2307",{"entities": [(25-7, 34-7, "MMAT")]}),
("fag  7205btvp bearing 003431603 stork",{"entities": [(12-7, 20-7, "MMAT")]}),
("bearing ball race nu307etvp2c3 fag  nu",{"entities": [(25-7, 37-7, "MMAT")]}),
("fag  6310 zz c3 bearing",{"entities": [(12-7, 22-7, "MMAT")]}),
("fag  6212 zz c3 bearing",{"entities": [(12-7, 22-7, "MMAT")]}),
("bearing 6009 2rsr c3 fag",{"entities": [(15-7, 27-7, "MMAT")]}),
("flanged bearing refsf79382z fag",{"entities": [(23-7, 34-7, "MMAT")]}),
("bearing kr19dz fag  kr19dz 112024",{"entities": [(15-7, 21-7, "MMAT")]}),
("bearing 62062rsva fag  62062rva 11430",{"entities": [(15-7, 24-7, "MMAT")]}),
("bearing 60022rsrc3 fag  60022rsrc3",{"entities": [(15-7, 25-7, "MMAT")]}),
("bearing nu2207etyp2 fag  nu2207etyp2",{"entities": [(15-7, 26-7, "MMAT")]}),
("fag  6219 bearing",{"entities": [(12-7, 16-7, "MMAT")]}),
("thrust bearing 51205 fag  make",{"entities": [(22-7, 27-7, "MMAT")]}),
("BEARING FAG 22212EKC3 SCRUBBER FAN EF2",{"entities": [(19-7, 28-7, "MMAT")]}),
("(BAKDCNTD) FAG Bearing 62082RSR",{"entities": [(30-7, 38-7, "MMAT")]}),
("BEARING 3206B",{"entities": [(15-7, 20-7, "MMAT")]}),
("CYLINDRICAL ROLLER BEARING NNF5020C 2LS",{"entities": [(34-7, 46-7, "MMAT")]}),
("BEARING 608 2Z",{"entities": [(15-7, 21-7, "MMAT")]}),
("BEARING FAG 6309C3",{"entities": [(19-7, 25-7, "MMAT")]}),
("BALL BEARING 205SZZG 9076 6205 2RS NR 62",{"entities": [(20-7, 27-7, "MMAT")]}),
("BEARING ROLLER 6004 2RSR FAG 60042RSH",{"entities": [(36-7, 44-7, "MMAT")]}),
("BEARING FAG 3209 B TNG",{"entities": [(19-7, 25-7, "MMAT")]}),
("BEARING 60102RS FAG",{"entities": [(15-7, 22-7, "MMAT")]}),
("(DSCNTD)BALL BEARING 6213 9573 FAG",{"entities": [(28-7, 32-7, "MMAT")]}),
("(DSCNTD)BALL BEARING 3313 9058 FAG",{"entities": [(28-7, 32-7, "MMAT")]}),
("FAG BEARING 6000 BRAMMER",{"entities": [(19-7, 23-7, "MMAT")]}),
("FAG BEARING 33210 BRAMMER",{"entities": [(19-7, 24-7, "MMAT")]}),
("BEARINGFAG 2306 2RS SELF ALIGNING",{"entities": [(18-7, 26-7, "MMAT")]}),
("FAG BEARING  RMS11 MRJ11/8",{"entities": [(20-7, 33-7, "MMAT")]}),
("FAG BEARING 60072RSR",{"entities": [(19-7, 27-7, "MMAT")]}),
("ROLLER BEARING 7310BUA FAG",{"entities": [(22-7, 29-7, "MMAT")]}),
("BEARING 62132RSRC3 FAG",{"entities": [(15-7, 25-7, "MMAT")]}),
("BEARING 3206B",{"entities": [(15-7, 20-7, "MMAT")]}),
("(DSCNTD)BEARING N 214 make=FAG makecode",{"entities": [(23-7, 28-7, "MMAT")]}),
("FAG BEARING NJ214ETVP2C3 BRAMMER",{"entities": [(19-7, 31-7, "MMAT")]}),
("FAG BEARING 60022RSR",{"entities": [(19-7, 27-7, "MMAT")]}),
("BEARINGROLLER FAG 21309KC3F TAPERED 45",{"entities": [(25-7, 34-7, "MMAT")]}),
("BEARING FAG 1208K C3 CLEARANCE",{"entities": [(19-7, 27-7, "MMAT")]}),
("(DSCNTD)BALL BEARING 6226 9101 FAG",{"entities": [(28-7, 32-7, "MMAT")]}),
("(DSCNTD)BALL BEARING FAG LS13AC 5337 (KI",{"entities": [(32-7, 38-7, "MMAT")]}),
("(DSCNTD) UVN58006363 BEARING  SLIDING",{"entities": [(16-7, 27-7, "MMAT")]}),
("(DSCNTD) 62142ZR BEARING  SEALED LJ 7",{"entities": [(16-7, 23-7, "MMAT")]}),
("(DSCNTD) KM 15 BEARING  LOCKNUT Make",{"entities": [(16-7, 21-7, "MMAT")]}),
("BEARING 3204B",{"entities": [(15-7, 20-7, "MMAT")]}),
("BEARING JK0S060",{"entities": [(15-7, 22-7, "MMAT")]}),
("BEARING 3208B",{"entities": [(15-7, 20-7, "MMAT")]}),
("FAG BEARING 60022RSR",{"entities": [(19-7, 27-7, "MMAT")]}),
("BEARING 6011 2RSR FAG",{"entities": [(20-7, 24-7, "MMAT")]}),
("BEARING BALL IMPERIAL 21/2X5X1 FAG",{"entities": [(29-7, 37-7, "MMAT")]}),

# iesa mmat training data, pass 1:
    #("93345|FESTO cylinder 63-80-PPVA-N3 sku: PKU-10003511|9/23/18|6|ea|181.02",{"entities": [(47-7, 59-7, "SKU")]}),
    #("00-3-A-F|SEW GEARBOX 60/1400RPM SEW SA57/T AD2 SA57/T AD2|P74-MOT-02186|SEW|SA57/T AD2",{"entities": [(65-7, 78-7,"SKU"),(83-7, 93-7, "MPN")]}),

'''

# LIB IMPORTS =================================
from __future__ import unicode_literals, print_function
import plac
import random
import sys
import os
import spacy
from spacy.util import minibatch, compounding
from spacy.tokens import Token
from spacy.pipeline import EntityRuler
from pathlib import Path

# IMPORT PATHS ================================
sys.path.append('../../../preprocessor/')

# .PY IMPORTS =================================
import loader
import string_cleaner

# GLOBALS  ====================================
# training data
TRAIN_DATA = [
    ("bearing n/roller sl0405018 (fag nnf5018b",{"entities": [(24-7, 33-7, "MMAT")]}),
    ("bearing slo45032 (fag ref nnf5032b.2ls.v",{"entities": [(15-7, 23-7, "MMAT")]}),
    ("(dscntd)ball bearing 3313 9058 fag",{"entities": [(28-7, 32-7, "MMAT")]}),
    ("(dscntd)ball bearing fag ls13ac 5337 (ki",{"entities": [(39-7, 43-7, "MMAT")]}),
    ("(dscntd)bearing 6202-2rs fag",{"entities": [(23-7, 31-7, "MMAT")]}),
    ("(dscntd) 6307-c3 bearing - . make - fag.",{"entities": [(16-7, 23-7, "MMAT")]}),
    ("(dscntd) 6317-zz-317pp bearing - ball. m",{"entities": [(16-7, 29-7, "MMAT")]}),
    ("fag bearing 22211-e1",{"entities": [(19-7, 27-7, "MMAT")]}),
    ("fag 6004zz bearing",{"entities": [(11-7, 17-7, "MMAT")]}),
    ("32213a bearing[manfcode32213a][manf=fag]",{"entities": [(7-7, 13-7, "MMAT")]}),
    ("3306a bearing[manfcode3306a][manf=fag][m",{"entities": [(7-7, 12-7, "MMAT")]}),
    ("ball bearing 6220c3 (preheater) mach=fag",{"entities": [(20-7, 26-7, "MMAT")]}),
]

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)

# FUNCTIONS  ==================================

# MAIN  =======================================
def main(model=None, output_dir="model_entRuler", n_iter=50):
    # setup pipeline
    # load the model you want to use
    # use nlp.disable_pipes to disable all pipes but NER

    """
    Load the model, set up the pipeline and train the entity recognizer.
    """
    if model is not None:
        nlp = spacy.load('model')  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        #nlp = spacy.load('en_core_web_sm', disable=['tagger', 'parser'])
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # ADD EXISTING/TRAINED ENTITY RULER  ----------------
    # load patterns from external file
    #nu_ruler = EntityRuler(nlp).from_disk('iesa_ners_patterns_mmat.jsonl')

    # putting the ruler before ner will override ner decisions in favor of ruler patterns
    #nlp.add_pipe(nu_ruler, before='ner')

    # show pipeline components:
    print(nlp.pipe_names)
    # --------------------------------------------------

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model

        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # show pipeline components:
    print(nlp.pipe_names)

    # end program
    print('Done.')

if __name__ == '__main__' :
    plac.call(main)
