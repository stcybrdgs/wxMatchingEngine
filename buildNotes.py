# BUILD NOTES

'''
TO DOs
RE: loader.loadDoc()  ---------------
The loader is designed to load one doc at a time. This approach
is fine for the ../io/ folder because it will only
have one doc in it per job (ie, the doc to be matched).
However, the folders in ../stores/ can contain multiples.
So, you need to setup a caller to select which doc(s)
from those multiple options are needed for the target
match job.

RE: preprocessor.import_csv(d)  --------------
is designed to import pipe delimitted docs. See if you
can enhance the function to use (or even detect) other
delimiters.

RE: preprocessor.import_csv(d)  --------------
The method at ../processor/loader.py > import_csv(d)
uses import csv to read csv files. It is common practice to use
import pandas as pd to deal with csv files -- explore the
advantages and swap in pandas if it seems useful.

-------------------------
MISC CODE

str.find(sub,start,end) # find substring
rem: os.listdir(path) returns a list object []
s.strip() # remove leading and trailing whitespace

RegEx example:
import re
list = ['item', 'thing', 'string']
for i in list:
    z = re.match('(g\w+)\W(g\w+)', i)
    if z: #do something

-------------------------

'''
