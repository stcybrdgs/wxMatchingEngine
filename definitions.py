'''
---------------------------------------
io/
    input/
    # contains file to be matched -> one per job
        tender.csv
    output/
---------------------------------------
ners/
    matcher.py
    # imports: []
        def matcher()
    trainer.py
    # imports: []
        def trainer()
---------------------------------------
preprocessor/
    loader.py
    # imports: [ csv, xlrd, os, sys ]
        def import_csv(d)
        def import_json(d)
        def import_pickle(d)
        def import_txt(d)
        def import_xls(d)
        def load_all()
        def loadDoc(d)
    stringCleaner.py
    # imports: [jellyfish, spacy, re, unicodedata2]
    # files: [ stop_words.txt ]
        def string_cleaner(d)
        def remove_accents(d)
        def remove_special_chars(d)
        def remove_whitespace(d)
        def normalizer(d)
        def lemmatizer(d)
        def porterStemmer(d)
---------------------------------------
processor/
    nlpObjectCreator.py
    # imports: [ spacy ]
        def create_nlp_object(d)
        def remove_stop_words(d)
    distanceEncoder.py
    # imports: []
        def levenshtein(s1, s2)
        def damerauLevenshtein(s1, s2)
        def jaro(s1, s2)
        def jaroWinkler(s1, s2)
        def hamming(s1, s2)
        def matchRatingComparison(s1, s2)
    phoneticEncoder.py
    # imports: []
        def soundex(s)
        def metaphone(s)
        def doubleMetaphone(s)
        def nysiis(s)
        def matchRatingCodex(s)
---------------------------------------
stores/
    lookups/
        bhSuppliers.json
    masters/
        erp10.csv
    models/
    pickles/
    taxonomies/
        bearings.json
        pumps.json
---------------------------------------
test/
        modulesMethods.json
        testController.py
        # imports: [ json, sys, importlib ]
'''
