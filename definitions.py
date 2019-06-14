'''
---------------------------------------
io/
    input/
        tender.csv
    output/
---------------------------------------
ners/
    matcher.py
        def matcher()
    trainer.py
        def trainer()
---------------------------------------
processor/
    distanceEncoder.py
        def levenshtein(s1, s2)
        def damerauLevenshtein(s1, s2)
        def jaro(s1, s2)
        def jaroWinkler(s1, s2)
        def hamming(s1, s2)
        def matchRatingComparison(s1, s2)
    loader.py
        def loadAll()
        def loadDoc(d)
    phoneticEncoder.py
        def soundex(s)
        def metaphone(s)
        def doubleMetaphone(s)
        def nysiis(s)
        def matchRatingCodex(s)
    preprocessor.py
        def preprocessor
    stringCleaner.py
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
'''
