'''
---------------------------------------
io/
    input/
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
processor/
    distanceEncoder.py
    # imports: []
        def levenshtein(s1, s2)
        def damerauLevenshtein(s1, s2)
        def jaro(s1, s2)
        def jaroWinkler(s1, s2)
        def hamming(s1, s2)
        def matchRatingComparison(s1, s2)
    loader.py
    # imports: [ csv, xlrd ]
        def import_csv(f)
        def import_txt(f)
        def import_xls(f)
        def loadAll()
        def loadDoc(d)
    phoneticEncoder.py
    # imports: []
        def soundex(s)
        def metaphone(s)
        def doubleMetaphone(s)
        def nysiis(s)
        def matchRatingCodex(s)
    preprocessor.py
    # imports: []
        def preprocessor
    stringCleaner.py
    # imports: []
        def porterStemmer(s)
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
