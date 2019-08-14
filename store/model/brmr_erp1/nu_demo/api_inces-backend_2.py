# -*- coding: utf-8 -*-
'''
Monday, August 12, 2019
Stacy Bridges
-   REM THIS SCRIPT HAS DIFFERENT API FRONT END THAN api_inces-backend.py
-	this script makes GET request from ince's backend (brammer, rs)
	https://api.ince.live/product?apikey=4f032b1a18ab3f36&id=6001&brand=skf
- 	the data pulled from the api is output to an excel spreadsheet (.xlsx)

APIKey = hardcoded for now
ID = the search string. Exact matches only but ignores special characters.
Not case sensitive.
Brand = optional

I've bodged together an option to query the supplier partcode for RS and Brammer

product?apikey=4f032b1a18ab3f36&supplier=RS&id=100-0151

Supplier must be 'RS' or 'Brammer'. Not case sensitive.
The ID will look against the supplier ID instead of the manufacturer ID.
Exact matches only. That's the WX-something codes for Brammer and the XXX-XXXX codes for RS.
If supplier is left out it'll work the same as before.
I've also set it scraping the codes from the gaps in the Hayley file that have
RS as the supplier as I don't have total coverage of the RS website yet. I've
got over 200k now, but still looks like there are quite a lot that I don't have.
Hopefully, that'll bump up our hit rate.

'''
# IMPORTS  ---------------------------------------------------------
import csv
import requests
import pandas as pd
from pandas import ExcelWriter
import numpy as np
import sys
import io

# UTF-8 Encoding  --------------------------------------------------
# allow printing of special characters to console without error
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# GLOBALS  ---------------------------------------------------------
mMats_test = []
mMats = []

# FUNCTIONS  -------------------------------------------------------
def import_csv(d):
	code = ''
	with open(d) as data:
		csv_reader = csv.reader(data, delimiter='|')
		i = 0
		for row in csv_reader:
			if i > 0:
				if len(row) == 0:
					code = ''
				else:
					code = row[0]
				mMats.append(code)
			i += 1
    # end function //

# MAIN  ------------------------------------------------------------
def main():
	# config  ------------------------------------------------------\\
	test = True
	mMats_test = ['121-084', '155-816','155-106']

	# config  ------------------------------------------------------//

	# define path to input file
	inFile = r'C:/Users/stacy/My GitHub/wxMatchingEngine/store/model/brmr_erp1/nu_demo/api_ince_backend_search_ids.csv'

	# define path to output file
	outFile = 'C:/Users/stacy/My GitHub/wxMatchingEngine/store/model/brmr_erp1/nu_demo/api_ince_backend_out.xlsx'
	outFile_test = 'C:/Users/stacy/My GitHub/wxMatchingEngine/store/model/brmr_erp1/nu_demo/api_ince_backend_out_test.xlsx'

	if test == True:
		pdFile = outFile_test
	else:
		pdFile = outFile

	# external id inputs
	import_csv(inFile)

	# clean special characters and spaces from codes in mMats[]
	special_chars = ['\\','/','-','.','_','+','"']
	i = 0
	for code in mMats:
		for char in special_chars:
			mMats[i] = code.strip().replace(char, '')
		i += 1

	# setup pandas containers to hold contents of xlsx columns
	# wBrand    |  wManufacturerPartNo  |  wSupplierId    |  wSource    |  wDescription    |  wDetails   |  wCategory
	# p_brands  |  p_manufacturerIds    |  p_supplierIds  |  p_sources  |  p_descriptions  |  p_details  |  p_categories
	p_brands = []  # field = wBrand
	p_manufacturerIds = []  # field = wManufacturerPartNo
	p_supplierIds = []  #  wSupplierId
	p_sources = []  # field = wSource
	p_descriptions = []  # field = wDescription
	p_details = []  # field = wDetails
	p_categories = []  # field = wCategory

	# set api-endpoint and parameters
	# product?apikey=4f032b1a18ab3f36&supplier=RS&id=100-0151
	# https://api.ince.live/product?apikey=4f032b1a18ab3f36&supplier=RS&id=121-084
	URL = "https://api.ince.live/product"
	apikey = '4f032b1a18ab3f36'
	supplier = 'RS'
	# brand = 'FESTO'

	i = 0
	if test == True:
		search_vals = mMats_test
	else:
		search_vals = mMats
	for code in search_vals:
		# send get request to api and save the response in a response object
		PARAMS = {'apikey':apikey, 'supplier':supplier, 'id':code}
		r = requests.get(url = URL, params = PARAMS)

		# extract the data in json format
		data = r.json()
		#print(data)  # test

		# check to see if the api responds to the id request
		try:
			supplierId = data[0]['supplierID']
		except:
			supplierId = 'id not found'

		# if api returns response to the id request,
		# it will return a list, so proceed by parsing
		# the list by looping through it index-wise
		# to retrieve brandStr as brand and descriptionStr as brand:manufacturerID:description
		if supplierId != 'id not found':
			# because the api may return multiple dictionaries for a single searchID,
			# we'll collect the results in list containers, and afterward append the lists
			# to the column containers for pandas
			# -------------------------------------------------------------------------------------------------------------------
			# wBrand    |  wManufacturerPartNo  |  wSupplierId    |  wSource    |  wDescription    |  wDetails   |  wCategory
			# p_brands  |  p_manufacturerIds    |  p_supplierIds  |  p_sources  |  p_descriptions  |  p_details  |  p_categories
			# -------------------------------------------------------------------------------------------------------------------
			j = 0
			brandStr = []
			descriptionStr = []
			sourceStr = []
			detailsStr = []
			for index in data:
				# collect results in list containers
				brandStr.append(data[j]['brand'])

				# handle errors where details return a null value
				try:
					details = data[j]['details']
				except:
					details = 'none'

				sourceStr.append(data[j]['source'])
				descriptionStr.append(data[j]['brand'] + ':' + data[j]['description'])
				detailsStr.append(data[j]['brand'] + ':' + str(details))

				# print results to console
				#print('{}: {} | {} | {} | {} | {}'.format(code,data[j]['source'],data[j]['brand'],data[j]['manufacturerID'],data[j]['description'],data[j]['details']))
				print()

				j += 1

			# print results to console
			print('{}: {} | {} | {} | {}'.format(code, sourceStr, brandStr, descriptionStr, detailsStr))


			# print results to pandas col arrays
			p_searchId.append(code)
			p_sources.append(sourceStr)
			p_brands.append(brandStr)
			p_descriptions.append(descriptionStr)
			p_details.append(detailsStr)

		else:
			# print results to console
			print('{}: empty'.format(code))

			# print results to pandas col arrays
			p_searchId.append(code)
			p_brands.append('')
			p_descriptions.append('')
			p_sources.append('')
			p_details.append('')

		i+= 1
	# end api call  //

	# print contents of pandas arrays to excel file (.xlsx)
	df = pd.DataFrame({'searchId':p_searchId, 'source':p_sources, 'brand':p_brands, 'description':p_descriptions, 'details':p_details})
	writer = pd.ExcelWriter(pdFile)
	df.to_excel(writer,'Product Data', index=False)
	writer.save()

	# end program
	print('Done.')

if __name__ == '__main__': main()
