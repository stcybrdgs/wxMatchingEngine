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
#("FAG DEEP GROOVE BALL BEARING 6026-2RSRC3", {"entities": [(0, 3, "SUPPLIER"), (4, 28, "PRODUCT"), (29, 40, "MPN")]}),
#("FAG RADIAL BALL BEARING 6321-C3", {"entities": [(0, 3, "SUPPLIER"), (4, 23, "PRODUCT"), (24, 31, "MPN")]}),
#("SKF CYLINDRICAL ROLLER BEARING N215ECP/C3", {"entities": [(0, 3, "SUPPLIER"), (4, 30, "PRODUCT"), (31, 41, "MPN")]}),
#("SKF NEEDLE ROLLER BEARING NKX20Z", {"entities": [(0, 3, "SUPPLIER"), (4, 25, "PRODUCT"), (26, 32, "MPN")]}),
#("SMC 5 PORT SOLENOID VALVE SV2100-5FUD", {"entities": [(0, 3, "SUPPLIER"), (4, 25, "PRODUCT"), (26, 37, "MPN")]}),
#("I NEED A 5 PORT SOLENOID VALVE BY SMC SV2100-5FUD", {"entities": [(0, 3, "SUPPLIER"), (34, 37, "PRODUCT"), (38, 49, "MPN")]}),
# train model on new suppliers: SIP, DISSTON as DISTON
# train model on new products:  Holesaw set, Holesaw, pump, water pump, dirty water pump, submersible dirty water pump
#("19724 SIP submersible dirty water pump 6819 12/15/2018 11 ft 342.43", {"entities": [(6,9, "SUPPLIER"), (22, 38, "PRODUCT")]}),
#("Submersible dirty water pump 6819 12/15/2018 11 ft 342.43", {"entities": [(0, 28, "PRODUCT"), (18, 28, "PRODUCT"), (24, 28, "PRODUCT")]}),
#("42788 8 piece holesaw set by Diston 4/19/2019 13 Ea 362.96", {"entities": [(29, 35, "SUPPLIER"), (6, 25, "PRODUCT"), (14, 25, "PRODUCT"), (14, 21, "PRODUCT")]}),
#("60646 Hi-tech 3 inch dirty water pump with 8 mm lift 12/25/2018 11 Ea 949.74", {"entities": [(21, 37, "PRODUCT")]})

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
    # train for sku:
    ("93345|FESTO cylinder 63-80-PPVA-N3 sku: PKU-10003511|9/23/18|6|ea|181.02",{"entities": [(47-7, 59-7, "SKU")]}),
    ("00-3-A-F|SEW GEARBOX 60/1400RPM SEW SA57/T AD2 SA57/T AD2|P74-MOT-02186|SEW|SA57/T AD2",{"entities": [(65-7, 78-7,"SKU"),(83-7, 93-7, "MPN")]}),
    ("FAG DEEP GROOVE BALL BEARING 6026-2RSRC3", {"entities": [(0, 3, "SUPPLIER"), (4, 28, "PRODUCT"), (29, 40, "MPN")]}),

    # re-train for product only
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
    ("22652|A lmi repair kit for a dosing pump in eff plant (sp-u6)|1/2/19|11|Ea|316.58",{"entities": [(19-7, 29-7, "PRODUCT")]})
]

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)

# FUNCTIONS  ==================================

# MAIN  =======================================
def main(model=None, output_dir="model", n_iter=50):
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
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # ADD EXISTIN/TRAINED ENTITY RULER  ----------------
    # load patterns from external file
    nu_ruler = EntityRuler(nlp).from_disk('ners_patterns_all.jsonl')

    # putting the ruler before ner will override ner decisions in favor of ruler patterns
    nlp.add_pipe(nu_ruler, before='ner')

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
