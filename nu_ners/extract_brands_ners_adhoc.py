#!/usr/bin/env python
# coding: utf8
# Compatible with: spaCy v2.0.0+
# extract_brands_ners_adhoc.py
"""
Wed, Oct 23, 2019
Stacy Bridges
"""
# EXTRACT BRANDS
# get data file input
# get brand input
# choose which data column to use for extraction
#    - program presents user with menu of options
# get fresh model
#    - use entity ruler and brands input to map brands
#    - chunk as needed
# get data column
#    - turn into nlp
#    - chunk as needed
# extract brands into single column
#    - extract as list of distinct brands
#    - if brands are already in the column, preserve them
# after extracting, run script to identify primary brand

# IMPORTS  =====================================
import os, sys, csv, json
import spacy
from spacy import displacy
from spacy.pipeline import EntityRuler
from spacy.pipeline import Tagger
from spacy.language import Language
from pathlib import Path
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lang.en.stop_words import STOP_WORDS
import pandas as pd
from pandas import ExcelWriter
import numpy as np

# PATHS  =======================================
#sys.path.append('../../../preprocessor')

# IMPORT PY FILES  =============================
import py_string_cleaner
import menu

# GLOBALS  =====================================
global row_heads
row_heads = []
df_tender = []
tender_col_choices = []
tender_col_nums = []

# FUNCTIONS  ===================================
def sentence_segmenter(doc):
    for token in doc:
        if token.text == 'wrwx':
            doc[token.i].is_sent_start = True
    return doc
    # end function //

def get_column_choice(tender_file):
    global df_tender
    # get the columns from the file
    # df.columns.tolist()
    tender_col_choices = []
    tender_col_nums = []
    df_tender = pd.read_excel(tender_file, sheet_name=0)  # read tender file into dataframe
    for head in df_tender:
        tender_col_choices.append(head)  # copy tender headers into array

    # print user menu
    print('\n-----------------------------------------')
    print('           Tender Columns')
    print('-----------------------------------------')
    spacer ='  '
    print('{}{}{}'.format('m', spacer, 'Show Main Menu'))
    tender_col_nums.append('m')
    col_num = ''
    i = 0
    for tc in tender_col_choices:
        i += 1
        print('{}  {}'.format(i, tc))
        tender_col_nums.append(str(i))

    # get user input
    print('\nSelect the column for extracting brands (or \'m\' for Main Menu)')
    col_choice = input()

    # validate user input
    while col_choice not in tender_col_nums:
        print('Invalid choice! Select a column (or \'m\' for Main Menu)')
        col_choice = input()

    if col_choice == 'm':
        menu.main()
        # if the user chooses 'm', then program control goes back to menu.main(),
        # which means that when menu.main() terminates, the program control will
        # return to this program; therefore, it's important to invoke sys.exit()
        # upon the callback to terminate all py execution in the terminal
        sys.exit()
    else:
        col_choice = tender_col_choices[int(col_choice)-1]
        print('\nYou chose: {}'.format(col_choice))
        #print(jsonl_files)

    return col_choice
    # end function //

def create_tender_csv(tender_file):
    global df_tender
    # get name of column that user wants to use to extract brands
    # and turn that colummn into a csv file
    # return the full path of the csv to the calling function
    column_choice = get_column_choice(tender_file) # get user's choice of column to extract brand from

    # get column_choice from tender_file and turn the col into a csv
    print('\nCreating csv file of selected tender column...\n')
    data = df_tender[column_choice]
    folder_path = os.path.dirname(os.path.abspath(__file__))
    csv_filename = folder_path + '\\' + 'brand_tender.csv'
    with open(csv_filename, 'w', encoding='utf-8') as outfile:  # encoding handles charmap errors
        outfile.write('description\n')
        for line in data:
            outfile.write(str(line) + '\n')
            #outfile.write('\n')
            print(line)

    print('\n\nThe selected data column was written to the csv file at:\n{}'.format(csv_filename))
    print('\nPress \'Enter\' to continue...')
    input()

    return csv_filename
    # end function //

def import_csv(d):
    global row_heads
    doc = ''
    with open(d) as data:
        csv_reader = csv.reader(data, delimiter='|')
        i = 0
        for row in csv_reader:
            # populate row_heads[]
            #if i > 0:  # skip header row
            row_head = row[0]
            row_heads.append(row_head)
            # populate txt obj
            doc = doc + 'wrwx ' + ('|'.join(row) + '\n')
            i += 1
    return doc
    # end function //

# MAIN  ========================================
def main(patterns_file, tender_file):
    '''
    NERS Demo w/ Sample Data
    '''
    print('module: extract_brands_ners_adhoc.py')
    print('\n')
    #print(patterns_file)
    #print(tender_file)
    #sys.exit()

    # CONFIG  -------------------------------------------------- \\
    # ------------------------------------------------------------ \\

    # brnd, mpn, spplr
    model = 'pre'   # pre -> use non-trained model / post -> use trained model
    brnd = 'on'  # on/off
    ruler = 'on'
    cleaner = 'on'
    number_tagger = 'off'

    # rem if stemmer is turned on after model does P2 training, then
    # you will need to use POS tag to detect nouns in products
    # then create new generator patterns for all.json
    # then run entity ruler again
    # stemmer = 'off'

    #outFile = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_brand_patterns.jsonl'
    # declare outputs
    # brnd_pandas_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_extracted_brands.xlsx'  # output
    # wx_1_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\test_data_cln_org_iesa_PPE_wx_v1.xlsx' # output

    # declare inputs
    #brnd_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\ners_brand_patterns.jsonl'  # input
    #patterns_file = brnd_file

    # rem tender_file = user-selected column from wx_1_file dataframe TENDER
    #tender_file = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\test_brands_old_input.csv'
    #tender_file = r'C:\Users\stacy\Desktop\NERS Demo\descriptions_nonstock.csv'
    write_type = 'w'

    # ------------------------------------------------------------ //
    # ---------------------------------------------------------- //

    # SETUP PD DATAFRAMES  -----------------------------------------------------
    # read Brands infile into pd dataframe
    # read Tender infile into pd dataframe

    # load model
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) #('en_core_web_sm', disable=['parser'])
    #elif model == 'post':nlp = spacy.load('demo_model')
    nlp.add_pipe(sentence_segmenter, after='tagger')

    # add pipes
    if ruler == 'on':
        # load patterns from external file only if model is not already trained
        nu_ruler = EntityRuler(nlp).from_disk(patterns_file)
        # putting the ruler before ner will override ner decisions in favor of ruler patterns
        nlp.add_pipe(nu_ruler)#, before='ner')
        '''
        # remember to swap precedence between ruler and ner after model training
        if model == 'post':
            # load patterns from external file only if model is not already trained
            if "entity_ruler" not in nlp.pipe_names:
                nu_ruler = EntityRuler(nlp).from_disk(patterns_file)
                # putting the ner before ruler will override favor ner decisions
                nlp.add_pipe(nu_ruler)#, before='ner')
        '''

    # ask user to select a column from the user-selected data file
    # and turn it into a csv file that can be imported by NERS
    tender_col_csv = create_tender_csv(tender_file)  # create the csv and return csv filename
    tender = import_csv(tender_col_csv)  # import the csv

    print('\nCleaning the tender input...')
    if cleaner == 'on':
        tender = py_string_cleaner.clean_doc(tender)  #  clean

    doc = nlp(tender)

    print('\nExtracting brands...')

    # show pipeline components:
    print(nlp.pipe_names)

    # COUNT ENTITIES  ----------------------------------------------------------
    labels = []
    alt_labels = []
    print('\n')
    labels = ['BRND']  # , 'PRODUCT', 'MPN', 'SKU']
    alt_labels = ['Brnd']  # , 'Product', 'MfrPartNo', 'SkuID']
    total_found = []
    total_unique_found = []
    for label in labels:
        tot_num = 0
        unique_num = 0
        unique = []
        for ent in doc.ents:
            # print([ent.text, ent.label_], end='')
            if ent.label_ == label:
                if ent.text not in unique:
                    unique.append(ent.text)
                    unique_num += 1
                tot_num += 1
        #print('\nFound {} total, {} unique.\n'.format(tot_num, unique_num))
        total_found.append(tot_num)
        total_unique_found.append(unique_num)

    # pandas output for brnds  ------------------------------------------------
    # This technique allows you to isolate entities on
    # a sentence-by-sentence basis, which will allow
    # for matching entities on a record-by-record basis
    wBrand_ext = []
    unique = []
    unique_str = ''
    existing_str = ''
    j = 0
    for sent in doc.sents:
        if j > 0:  # no need to process the header
            existing_str = str(df_tender['wBrand_all'][j-1]).lower()  # !!! ------------------------ !!!
            if existing_str == 'nan':  # !!! ------------------------ !!
                existing_str = ''  # !!! ------------------------ !!
            for ent in sent.ents:
                if ent.label_ == 'BRND':
                    # add condition 'and (existing_str.find(ent.text) < 0)'
                    # to account for any brands already extracted by prior runs
                    if ent.text not in unique and (existing_str.find(ent.text) < 0):  # !!! -------- !!!
                        unique.append(ent.text)
            brnd_count = 0
            for brnd in unique:
                delimiter = ''
                brnd_count += 1
                if brnd_count == len(unique):
                    brnd_delimiter = ''
                else:
                    brnd_delimiter = ', '
                unique_str = unique_str + brnd + brnd_delimiter
            if existing_str != '' and unique_str != '':
                unique_str = existing_str + ', ' + unique_str  # add new brands to those from prior runs  # !!! -------- !!!
            elif existing_str != '' and unique_str == '':
                unique_str = existing_str
            unique_str = unique_str.upper()
            # trim trailing commas
            #if unique_str[len(unique_str)-1:len(unique_str)] == ',':  # !!! -------- !!!
            #    unique_str = unique_str[0:len(unique_str)-1]  # !!! -------- !!!
            wBrand_ext.append(unique_str)
            print(j)  # print record account to console
            unique.clear()  # reset var for next record
            unique_str = '' # reset var for next record
        j += 1

        # FOR THE CHUNKER
        # It basically creates a new dataframe object with the new data row
        # at the end of the dataframe. The old dataframe will be unchanged.
        # data = [{'Region':'East','Company':'Shop Rite','Product':'Fruits','Month':'December','Sales': 1265}]
        # df.append(data,ignore_index=True,sort=False)

        # DataFrame.insert(self, loc, column, value, allow_duplicates=False)
        # loc : int # insertion index, must verify0 <= loc <= len(cols)
        # column: string, number, or hashable object -- this is label of inserted col
        # value: int, Series, or array-like
        # allow_duplicates: bool, optional

    # SETUP DATAFRAME  ---------------------------------------------------------
    # first, combine newly extracted brands with any brands that already exist
    # in the wBrand_all column of the wx_v1 file
    '''
    nu_wBrand_all = []  # use this [] to combine wBrand_ext with wBrand_all
    nu_unique = []
    for row in df_tender[wBrand_all]:
        for str in row
        if
    '''

    df_ofile = r'C:\Users\stacy\Desktop\IESA Project - Europe\IESA Phase 2\ners\db_data_cln_org_iesa_PPE_wx_v1.xlsx'
    df_del_dict = {}
    for head in df_tender:
        if head == 'wBrand_all':
            df_del_dict.update({head:wBrand_ext})
        else:
            df_del_dict.update({head:df_tender[head]})
    df_del = pd.DataFrame(df_del_dict)
    writer = pd.ExcelWriter(df_ofile)
    df_del.to_excel(writer, 'TestData', index=False)
    writer.save()

    # save the model  ----------------------------------------------------------
    # save model with entity pattern updates made by the entity ruler
    output_dir = Path('ners_adhoc_model')
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)

    print("\nNERS Model was saved to ", output_dir)
    print('Extracted Brands saved to:\n', df_ofile)
    # TEST  -----------------------------
    #mpns = []

    # DISPLACY VISUALIZER  -----------------------------------------------------
    # get results for html doc
    results = ''
    i = 0
    for item in alt_labels:
        results = results + '{}: {} tot  {} unq\n'.format(item, total_found[i], total_unique_found[i])
        i += 1
    # store nlp object as string in html var
    spacer = '---------------------------------------------------------\n'
    header = 'Named Entities Found in Target File:\n'
    doc = nlp(header + spacer + results + spacer + tender)
    doc.user_data["title"] = "Named Entity Resolution System (NERS)"
    colors = {"BRND": "#FFDDA1"}
    #colors = {"MPN": "#C3FFA1", "BRND": "#FFDDA1", "CMMDTY": "#F3DDA1"}
    options = {"ents": ["MPN", "BRND", "CMMDTY"], "colors": colors}
    # displacy.serve(doc, style="ent", options=options)
    html = displacy.render(doc, style="ent", page=True, options=options)  # use the entity visualizer
    # write the html string to the xampp folder and launch in browser through localhost port
    with open('C:/Users/stacy/Desktop/IESA Project - Europe/IESA Phase 2/ners/displacy/index.html', 'w') as data:
        data.write(html)

    print('\n' + results)


    # end program
    print('Done.')

if __name__ == '__main__' : main()
