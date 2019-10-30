import pandas as pd
from pandas import ExcelWriter
import numpy as np

#def get_column_choice(tender_file):
# get the columns from the file
# df.columns.tolist()

tender_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\db_data_cln_org_iesa_PPE_wx_v1.xlsx'
tender_col_choices = []
tender_col_nums = []

oBrand_all_in = []
wBrand_all_in = []
wBrand_all_out = []

df_tender = pd.read_excel(tender_file, sheet_name=0)  # read tender file into dataframe

for head in df_tender:
#    print(head, df_tender[head].count())  # get count of records in each column
    if head == 'oBrand':
        for row in df_tender[head]:
            oBrand_all_in.append(row)
    if head == 'wBrand_all':
        for row in df_tender[head]:
            wBrand_all_in.append(row)

brands = ['skf', 'cooper', 'smc', 'centurion']
unique = ['skf', 'centurion']
existing = ''
i = 0
for b in brands:
    existing = str(df_tender['wBrand_all'][i]).lower()
    if b not in unique and (existing.find(b) < 0):
        print(i, '  ', b)
    else:
        print(i, '   no uniques')
    i += 1

for i in range(0,5):
    s = df_tender['wBrand_all'][i]
    print(str(s).lower())
    if str(s) == 'nan': print('NAN')
