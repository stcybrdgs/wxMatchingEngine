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

string_cleaner needs to add:
chunking
coreference resolution rem neural coref

LU try / except error handling-- for example:
     try:
         d = unicode(d, 'utf-8')
     except (TypeError, NameError): # unicode is a default on python3
         pass

RE: processor
processor.py > create_nlp_object(d)
needs to add language detection
so it knows which model to load

rem 'sm' model has no word2vector capability

# rem future method() for pulling suppliers lookup from master
# def trainer():
# train md_erp on phonetic and distance encoding
# train md_erp on suppliers
# (for future sprint, do pickles and persistend store)
# train tender on phonetic and distance encoding

MULTIPROCESSING
Multiprocessing means that several processes are executed simultaneously,
usually over several Central Processing Units (CPUs) or CPU cores, thus
saving time. An example is the training of machine learning models or neural
networks, which are intensive and time-consuming processes. By distributing
these on a large amount of processing units, a lot of time can be saved.
In Python, this is done using the multiprocessing package.

REM STOP WORDS
# remove stop words from doc object
#   stop words are most common filter words
#   rem matching tokens will return True for is_stop
#   you need to create nlp object before working with stop words
#   because the doc needs to be tokenized
I CHOSE TO NOT USE SPACY STOP_WORDS BUT INSTEAD TO REMOVE THE WORDS
DIRECTLY FROM THE INPUT DOC BEFORE TURNING IT INTO AN NLP OBJECT


-------------------------
ADD CUSTOM STOP WORDS IN SPACY
customize_stop_words = [
    'computing', 'filtered'
]
for w in customize_stop_words:
    spacy_nlp.vocab[w].is_stop = True
doc = spacy_nlp(article)
tokens = [token.text for token in doc if not token.is_stop]
print('Original Article: %s' % (article))
print()
print(tokens)


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

STOP_WORDS
from spacy.lang.en.examples import sentences
from spacy.lang.en.stop_words import STOP_WORDS
print(STOP_WORDS)  # TEST ONLY
{'alone', 'ca', 'hereafter', 'two', 'almost', 'never', 'up', 'wherein', 'four', 'each', 'ours', 'that', 'though', 'latterly', 'ever', 'beforehand', 'itself', 'what', 'take', 'quite', 'most', 'least', 'together', 'nobody', 'every', 'again', 'no', 'is', 'thus', 'for', 'thereafter', 'anyway', 'you', 'any', 'well', 'has', 'will', 'only', 'whoever', 'somehow', 'latter', 'down', 'namely', 'have', 'these', 'cannot', 'six', 'sometime', 'before', 'forty', 'seemed', 'amongst', 'so', 'against', 'whole', 'once', 'can', 'who', 'therefore', '�ve', 'if', 'at', 'used', 'wherever', "'s", 'either', 'make', 'then', 'name', 'few', 'see', 'among', 'does', 'be', 'fifty', 'anyhow', '�ll', "'re", 'noone', 'elsewhere', 'get', '�re', 'nevertheless', 'onto', 'ourselves', 'first', 'do', 'around', 'seeming', 'throughout', 'someone', 'than', 'through', 'whose', "n't", 'nowhere', 'other', 'move', "'d", 'therein', 'are', 'those', 'thence', 'top', 'behind', 'myself', 'himself', 'upon', 'put', 'rather', 'them', 'which', 'not', 'too', 'others', 'afterwards', '�m', 'amount', "'ll", 'now', 'due', 'another', 'anything', 'otherwise', 'into', 'none', 're', 'by', 'less', 'one', 'eight', 'becomes', 'also', 'must', '�s', 'keep', 'except', 'hereupon', 'beside', 'sometimes', 'n�t', "'m", '�re', 'such', 'third', 'enough', 'off', 'whatever', 'thereby', 'anywhere', 'were', 'hence', 'somewhere', 'call', 'out', 'may', 'your', 'beyond', 'much', 'why', 'perhaps', 'there', 'still', 'whenever', 'him', 'hundred', 'give', 'with', 'their', 'however', 'where', 'after', 'say', 'was', 'being', 'whither', 'yourselves', 'already', 'while', 'everywhere', 'via', '�m', 'both', 'side', 'n�t', 'whereupon', 'would', 'various', 'hers', 'please', 'her', 'how', 'five', 'could', 'show', 'about', 'along', 'moreover', 'serious', 'yourself', 'thereupon', 'empty', 'although', 'between', 'whereafter', 'twelve', 'whether', 'full', 'herein', 'go', 'else', 'me', 'because', 'herself', '�ve', 'an', 'same', 'besides', 'mine', 'fifteen', 'should', 'might', 'several', 'unless', 'own', 'am', 'his', 'nothing', 'became', 'often', 'as', 'more', 'part', 'front', 'even', 'become', 'across', 'under', 'whom', 'always', 'of', 'within', 'becoming', '�ll', 'twenty', 'formerly', 'just', '�d', 'whence', 'and', 'below', 'above', 'the', 'during', 'its', 'it', 'very', 'on', 'regarding', 'next', 'had', 'toward', 'from', 'here', 'he', 'but', 'did', 'former', 'whereby', 'really', 'further', 'us', 'ten', 'this', 'until', 'whereas', 'back', 'since', 'hereby', 'anyone', 'seems', 'i', '�s', 'bottom', 'towards', 'everything', 'our', 'been', 'something', 'using', 'nor', 'many', 'in', "'ve", 'doing', 'without', 'or', 'sixty', 'last', 'nine', 'made', 'themselves', 'she', 'my', 'over', 'mostly', 'a', 'meanwhile', 'when', '�d', 'per', 'yours', 'they', 'three', 'to', 'some', 'we', 'eleven', 'seem', 'indeed', 'yet', 'everyone', 'thru', 'neither', 'all', 'done'}

GITHUB
when your local gets one step behind remote:
git fetch --all --prune
git merge origin branch1
-------------------------

'''
