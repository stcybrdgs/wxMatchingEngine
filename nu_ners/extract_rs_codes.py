"""
Thur Nov 7, 2019
Stacy Bridges

This script searches through a user-selected column of input data to extract
regex patterns resembling RS product codes. The results are printed to the
console and also written back to the project file that contains the original
column of input data. The output is written to a column called RS_Codes.

"""
# import libraries  ============================================================
import re, os, sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

# helper functions  ============================================================
# clean_result()
# cleans the regex result of any leading/trailing chars and returns result to caller
def clean_result(result):
    stop_chars = [' ', ',', '(', '{', '[', ')', '}', ']', 'RS', ':']
    token = ''
    for char in result[0]:
        if char not in stop_chars:
            token = token + char
    return token
    # end function //

def string_to_token_list(string):
    token_list = []
    comma_loc = string.find(',')
    if comma_loc < 0:
        token_list.append(string)
    else:
        not_end_of_string = True
        while not_end_of_string:
            # put token into list
            start_loc = 0
            end_loc = comma_loc
            token_list.append(string[start_loc:end_loc])

            # truncate string
            string = string[comma_loc+2:len(string)]
            comma_loc = string.find(',')

            if comma_loc < 0:
                # if you are at last token, insert it
                end_loc = len(string)
                token_list.append(string[start_loc:end_loc])
                not_end_of_string = False

    return token_list
    # end function //

# globals  =====================================================================
# identify regex search patterns
#[\s,({[]RS\d{3}[-]\d{3,4}[\s,)}]',  # # case 4: the regex is inline preceded by 'RS'
rs_regex_strings = [
    '[\s,:({[]\d{3}[-]\d{3,4}[\s,)}]',  # # case: the regex is inline
    '^\d{3}[-]\d{3,4}[\s,)}]',  # case: the regex is at start of line
    '[\s,({[]\d{3}[-]\d{3,4}$',  # case: the regex is at end of line
    '^\d{3}[-]\d{3,4}$'  # case: the regex is at start of line and no chars trail it
]

# main  ========================================================================
def main(file_name, col_name):
    print('\nExtracting RS Codes...')
    global rs_regex_strings

    # get input file
    folder_path = os.path.dirname(os.path.abspath(__file__))
    infile = folder_path + '\\' + file_name
    outfile = infile

    # get dataframe/column
    df_tender = pd.read_excel(infile, sheet_name=0)  # read file into dataframe
    df_headers = df_tender.columns
    tender = df_tender[col_name]  #mpns = df_tender['ManufacturerPartNo']

    # if a wRS_Code col exists in the data, preserve it, else start a blank one
    wRS_Code = []
    if 'wRS_Code' in df_headers:
        for code in df_tender['wRS_Code']:
            wRS_Code.append(code)

    # find rs codes  -----------------------------------------------------------
    # find rs codes per regex rules and store them in results array; afterward,
    # we will merge wRS_Code[] with results[] to yield the final data column
    results = []
    result_count = 0
    rgx = 0
    for regex in rs_regex_strings:
        if rgx == 0:
            # on first rgx pass, results[] is empty, so populate it w/o performing comparisons
            for row in tender:
                result = re.findall(regex, str(row))  # get regex result, if any
                # if the regex pattern is found, then clean it and add it to results[]
                # else add '' to results[]
                if result:
                    result_count += 1
                    result = clean_result(result) # clean the result
                    results.append(result)
                    print(result)
                else:
                    results.append('null')
        else:
            i = 0
            for row in tender:
                result = re.findall(regex, str(row))  # get regex result, if any
                if result:
                    result_count += 1
                    result = clean_result(result)
                    print(result)
                    if results[i] == 'null':
                        # case: if results[i] == 'null' then insert result
                        results[i] = result
                    elif results[i] != result:
                        # case: if results[i] != result then add new result to index
                        results[i] = results[i] + ', ' + result
                    else:
                        # case: results[i] == result (no action required)
                        pass
                i += 1
        rgx += 1

    # merge results[] with wRS_Code[]  -----------------------------------------
    if len(wRS_Code) == 0:
        # if wRS_Code is empty, copy results into it
        i = 0
        for r in results:
            if r == 'null':
                results[i] = ''
            i += 1
        wRS_Code = results
    else:
        # convert results[] from a list of strings into a list of token lists
        i = 0
        for result in results:
            results[i] = string_to_token_list(result)
            i += 1

        # compare results[] to wRS_Code[] strings and add any unique tokens that
        # don't already exist in wRS_Code[]
        i = 0
        for list in results:
            nu_rs_code = str(wRS_Code[i])
            if nu_rs_code == 'nan':
                nu_rs_code = ''
            for token in list:
                token = str(token)
                if token == 'null':
                    token = ''
                if token != '':
                    if nu_rs_code == '':
                        nu_rs_code = token
                    elif nu_rs_code.find(token) < 0:
                        nu_rs_code = nu_rs_code + ', ' + token
            wRS_Code[i] = nu_rs_code
            i += 1

    # write data to project file  ----------------------------------------------
    p_dict = {}
    for head in df_tender:
        if head == 'wRS_Code':
            p_dict.update({head:wRS_Code})
        else:
            p_dict.update({head:df_tender[head]})

    if 'wRS_Code' not in df_headers:
        p_dict.update({'wRS_Code':wRS_Code})

    df_out = pd.DataFrame(p_dict)
    writer = pd.ExcelWriter(outfile)
    df_out.to_excel(writer, 'TestData', index=False)
    writer.save()

    # end program
    print('\n{} results written'.format(result_count))
    print(file_name)
    print(outfile)
    print('\nDone.')

if __name__ == '__main__' : main()
