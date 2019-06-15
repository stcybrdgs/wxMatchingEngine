# BUILD NOTES

# MISC CODE  ===============================
# str.find(sub,start,end) # find substring
# rem: os.listdir(path) returns a list object []

'''
TO DOs
RE: loader.loadDoc()  ---------------
The method at ../processor/loader.py > loadDoc(d)
is designed to load one doc at a time. This approach
is fine for the ../io/ folder because it will only
have one doc in it per job (ie, the doc to be matched).
However, the folders in ../stores/ can contain multiples.
So, you need to setup a caller to select which doc(s)
from those multiple options are needed for the target
match job.

'''
