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
    # imports: [ xlrd, csv, os, sys, re ]
        # helper functions
            def get_path(d)
            def import_json(d)
            def import_pickle(d)
            def import_xls(d)
            def import_csv(d)
            def import_txt(d)
        # controller function
            def load_doc(d)
    string_cleaner.py
    # imports: [ unicodedata2, re ]
        # helper functions
            # def lemmatizer(d)
            def remove_accents(d)
            def remove_special_chars(d)
            def remove_whitespace(d)
            def normalizer(d)
        # controller function
            def string_cleaner(d)
---------------------------------------
processor/
    distance_encoder.py
    # imports: [ jellyfish ]
        def levenshtein(s1, s2)
        def damerau_levenshtein(s1, s2)
        def jaro(s1, s2)
        def jaro_winkler(s1, s2)
        def hamming(s1, s2)
        def match_rating_comparison(s1, s2)
    phonetic_encoder.py
    # imports: [ sys, jellyfish, doublemetaphone ]
        def soundex(s)
        def metaphone(s)
        def double_metaphone(s)
        def nysiis(s)
        def match_rating_codex(s)
    nlp_object_processor.py
    # imports[ spacy, STOP_WORDS ]
        # helper functions
            def remove_stop_words(d)
        # controller function
            def create_nlp_object(d)
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
