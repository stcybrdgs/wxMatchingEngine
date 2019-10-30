import pandas as pd
from pandas import ExcelWriter
import numpy as np

#def get_column_choice(tender_file):
# get the columns from the file
# df.columns.tolist()

tender_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\db_data_cln_org_iesa_PPE_wx_v1.xlsx'
tender_col_choices = []
tender_col_nums = []

df_tender = pd.read_excel(tender_file, sheet_name=0)  # read tender file into dataframe
for head in df_tender:
    tender_col_choices.append(head)  # copy tender headers into array

for head in tender_col_choices:
    print(head, df_tender[head].count())  # get count of records in each column

print(df_tender['ID'].count())

# oMPN   7996
# ovMPN 15593
ofile = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\00_test_pd_output.xlsx'
df_del_dict = {}
for head in df_tender:
    if head == 'wKeyWords':
        df_del_dict.update({head:'Success!'})
    else:
        df_del_dict.update({head:df_tender[head]})
df_del = pd.DataFrame(df_del_dict)
writer = pd.ExcelWriter(ofile)
df_del.to_excel(writer, 'TestData', index=False)
writer.save()
