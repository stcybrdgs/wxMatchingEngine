import re
import csv
import pandas as pd
from pandas import ExcelWriter
import numpy
import xlsxwriter
import os

mpn_desc = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\test\regExTool\ManufDesc.csv'
brnd_stop = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\test\regExTool\additional_stopwords.csv'
regex_set = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\test\regExTool\regExpressionList.csv'
outfile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\eriks\test\regExTool\regOutput.xlsx'

#open CSV file containing manufacturerID
with open(mpn_desc) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    ManufDesc=pd.DataFrame(readCSV)
print(ManufDesc.head())

#open CSV file containing brand_names_stopwords
with open(brnd_stop) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    string=""
    stop_words=[]
    for row in readCSV:
        string=string.join(row)
        stop_words.append(string)

#open CSV file containing regualr expression list
with open(regex_set) as regExpCSV:
  regExpList = csv.reader(regExpCSV, delimiter='\n')
  string=""
  x=[]
  for row in regExpList:
      string=string.join(row)
      x.append(string)
reExp='|'.join(x)

###--------clean manuf Descriptions by removing stopwords------------#########
import nltk
nltk.download('stopwords')
import string
from nltk.corpus import stopwords

#creating custom stopword list by appending brand names and the word bearing
stop = stopwords.words('english')
#extra_stopwords=['safety','bearing','bearings','bearing.','bearings.','bearing:','bearings:','belt','contactor','circuit','breaker','switch','air','valve','limit','line','overload']
[stop.append(i) for i in stop_words]
#[stop.append(extra_stopwords)]
print(stop)
#remove stopwords
for i in range(0,ManufDesc.index[-1]):
    ManufDesc[0][i]=[word.replace(","," , ").replace("."," . ").replace(")"," ) ") for word in ManufDesc[0][i].split()]
    ManufDesc[0][i]=' '.join(ManufDesc[0][i])
    ManufDesc[0][i]=[word for word in ManufDesc[0][i].split() if word.lower() not in stop]
    ManufDesc[0][i]=' '.join(ManufDesc[0][i])

###-------------------------CONFIG-------------##########
RS_regex='^\d{3}[ -]\d{3,4}|[ ]\d{3}[ -]\d{3,4}'
#all_regex='\d{1}\w{1,3}[/ -X]*\d{1}\w{0,4}[/ -X]\w{0,4}\d*[ ]|\w{1,3}\d+[/ -.]*[X]*\w{0,2}\d*[- .]*[/]*\w{0,2}\d+|\(\d+\w{0,4}[ -.]*\d+\w*\)|\d+[/ -.]*\d+|\d+[- . ][a-zA-Z]{1,4}|\d+[-.XMm ]\w{1,2}[ mM]*\d+[ XmM]*\d*[mM ]*|\w{1,2}[/]*\d+\w{0,4}[/]*\d+|\w{1,4}[/ -.]\d+[/ .-]\d+[/ -.]*\d*|\w{2,3}[- .]*\d+\w{0,2}\d+[ ]|\w{1,3}\d+[a-zA-Z]{0,4}\d*[a-zA-Z]{0,4}\d*[a-zA-Z]{0,4}\d*[a-zA-Z]{0,4}\d*[a-zA-Z]{0,4}\d*|\d+'

###--------------------FUNCTIONS----------------########
regex_RS = lambda x: re.findall(RS_regex,str(x))
regex_all = lambda x: re.findall(reExp,str(x))
clean= lambda x: str(x).replace('[','').replace(']','').replace("'",'').replace('"','').replace('(','').replace(')','')

all=[]
all= ManufDesc[0].apply(regex_all)
all.str.strip() ##---remove whitespace

RS=[]
RS = ManufDesc[0].apply(regex_RS)
RS.str.strip() ##---remove whitespace

# create data frame
df = pd.DataFrame({
    'All_Results': all.apply(clean),
    'RS codes': RS.apply(clean),
    'ManufDesc': ManufDesc[0]
})

# write to excel file
# create writer
writer = pd.ExcelWriter(outfile)
# write to file

df.to_excel(writer, 'Manuf Codes', index=False)
# save
writer.save()

# end program
print(' \n Successfull!')
