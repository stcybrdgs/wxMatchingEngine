# -*- coding: utf-8 -*-
'''
Monday, August 19, 2019
Stacy Bridges

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
					code = 'x'
				else:
					code = row[0]
				mMats.append(code)
			i += 1
    # end function //

# MAIN  ------------------------------------------------------------
def main():
	# config  ------------------------------------------------------\\
	test = True
	mMats_test = [ '445-0926', '493-0236', 'x', 'x', '193-026' ]

	'''
	[
		'2201 2RS TV',
		'2201 2RS TV',
		'3210B 2RSR TVH',
		'6004 2 RSR',
		'6207 2ZR',
		'6303 2ZR C3',
	]
	'''

#		'6201-2Z','62012Z','624-2Z','6001','6003-2RSH','608-2Z','61800', '111-3719', '61800', 'ZCMD21L2']

	# config  ------------------------------------------------------//
	# define path to input file
	inFile = r'C:/Users/stacy/My GitHub/wxMatchingEngine/store/model/brmr_erp1/eriks/input/in_api_ince_backend_search_ids.csv'

	# define path to output file
	outFile = 'C:/Users/stacy/My GitHub/wxMatchingEngine/store/model/brmr_erp1/eriks/output/out_api_ince_backend.xlsx'
	outFile_test = 'C:/Users/stacy/My GitHub/wxMatchingEngine/store/model/brmr_erp1/eriks/test/out_api_ince_backend_test.xlsx'

	if test == True:
		pdFile = outFile_test
	else:
		pdFile = outFile

	# external id inputs
	if test == False:
		import_csv(inFile)

	# setup pandas containers to hold contents of xlsx columns
	# wBrand    |  wManufacturerPartNo  |  wSupplierId    |  wSource    |  wDescription    |  wSupplementalDetails   |  wCategory        |  wStatus
	# p_brands  |  p_manufacturerIds    |  p_supplierIds  |  p_sources  |  p_descriptions  |  p_details  			 |  p_categories	 |  wStatus
	p_brands = []  # field = wBrand
	p_manufacturerIds = []  # field = wManufacturerPartNo
	p_supplierIds = []  #  wSupplierId
	p_sources = []  # field = wSource
	p_descriptions = []  # field = wDescription
	p_details = []  # field = wSupplementalDetails
	p_categories = []  # field = wCategory
	p_status = []  # field = wStatus

	# set api-endpoint and parameters
	# product?apikey=4f032b1a18ab3f36&supplier=RS&id=100-0151
	# https://api.ince.live/product?apikey=4f032b1a18ab3f36&supplier=RS&id=121-084
	# https://api.ince.live/product?apikey=4f032b1a18ab3f36&id=60032-RSH
	URL = "https://api.ince.live/product"
	apikey = '4f032b1a18ab3f36'
	supplier = 'RS'

	if test == True:
		search_vals = mMats_test
	else:
		search_vals = mMats

	i = 0
	for code in search_vals:
		if code == 'x':
			print(code, ': empty')
			p_brands.append('')
			p_manufacturerIds.append('')
			p_supplierIds.append('')
			p_sources.append('')
			p_descriptions.append('')
			p_details.append('')
			p_categories.append('')
			p_status.append('')
			i += 1
			continue

		elif code != 'x':
			#print(code)  # test
			# send get request to api and save the response in a response object
			#PARAMS = {'apikey':apikey, 'supplier':supplier, 'id':code}
			PARAMS = {'apikey':apikey, 'supplier': supplier, 'id':code}
			r = requests.get(url = URL, params = PARAMS)

			# extract the data in json format
			# handle code 500 server error
			try:
				data = r.json()
			except:
				data = 'Status code 500'
				print('{}: {}:{}'.format(code, 'server error', '[500]'))
				# print results to pandas col arrays
				p_brands.append('')
				p_manufacturerIds.append('')
				p_supplierIds.append('')
				p_sources.append('')
				p_descriptions.append('')
				p_details.append('')
				p_categories.append('')
				p_status.append('')
				i += 1
				continue

			# check to see if the api responds to the id request
			try:
				searchId = data['searchID']  # searchId = data[0]['searchID']
			except:
				searchId = 'id not found'

			# if api returns response to the id request,
			# it will return a list, so proceed by parsing
			# the list by looping through it index-wise
			# to retrieve brandStr as brand and descriptionStr as brand:manufacturerID:description
			if searchId != 'id not found':

				print(code, '  ', end = '')
				print(data['brand'])
				print('{}: {}: {}'.format(r, data['searchID'], data))  # TEST -----------------------

				# because the api may return multiple dictionaries for a single searchID,
				# we'll collect the results in list containers, and afterward append the lists
				# to the column containers for pandas; the mapping is:
				# -------------------------------------------------------------------------------------------------------------------------------------------------------
				# api key:		brand	  |  manufacturerID	    |  supplierID     |  source     |  description     |  details    			|  productCategory	|
				# wx field:		wBrand    |  wManufacturerId    |  wSupplierId    |  wSource    |  wDescription    |  wSupplementalDetails 	|  wCategory		| wStatus
				# py container:	p_brands  |  p_manufacturerIds  |  p_supplierIds  |  p_sources  |  p_descriptions  |  p_details  			|  p_categories		|
				# -------------------------------------------------------------------------------------------------------------------------------------------------------
				detailsStr = []

				# handle errors where details return a null value
				try:
					details = data[0]['details']
				except:
					details = 'none'

				# print results to console
				print('{}: {} | {} | {} | {} | {} | {} | {}'.format(
					code, data['brand'], data['manufacturerID'],
					data['supplierID'], data['source'], data['description'],
					details, data['productCategory']))
				'''
				print('{}: {} | {} | {} | {} | {} | {} | {}'.format(
					code, data[0]['brand'], data[0]['manufacturerID'],
					data[0]['supplierID'], data[0]['source'], data[0]['description'],
					details, data[0]['productCategory']))
				'''

				# print results to pandas col arrays
				p_brands.append(data['brand'])  # (brandStr)
				p_manufacturerIds.append(data['manufacturerID'])
				p_supplierIds.append(data['supplierID'])
				p_sources.append(data['source'])
				p_descriptions.append(data['description'])  # (descriptionStr)
				p_details.append(details)
				p_categories.append(data['productCategory'])
				p_status.append('External')

			else:
				# print results to console
				print('{}: empty'.format(code))

				# print results to pandas col arrays
				p_brands.append('')
				p_manufacturerIds.append('')
				p_supplierIds.append('')
				p_sources.append('')
				p_descriptions.append('')
				p_details.append('')
				p_categories.append('')
				p_status.append('')

			i+= 1
		# end api call  //

	# clean up details
	'''
	j = 0
	for item in p_details:
		# if there are details returned by api, clean them up before
		# printing them to the excel file
		if p_details[j] != '':
			nuDetail = p_details[j]
			nuDetail = nuDetail.replace('- Bore', 'Bore')
			nuDetail = nuDetail.replace('- Width', ', Width')
			nuDetail = nuDetail.replace('- Outer', ', Outer')
			nuDetail = nuDetail.strip()
			p_details[j] = nuDetail
		j += 1
	'''

	# print contents of pandas arrays to excel file (.xlsx)
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------
	# api key:		brand	  |  manufacturerID	    |  supplierID     |  source     |  description     |  details    			|  productCategory	|
	# wx field:		wBrand    |  wManufacturerId    |  wSupplierId    |  wSource    |  wDescription    |  wSupplementalDetails 	|  wCategory		|  wStatus
	# py container:	p_brands  |  p_manufacturerIds  |  p_supplierIds  |  p_sources  |  p_descriptions  |  p_details  			|  p_categories		|
	# ---------------------------------------------------------------------------------------------------------------------------------------------------------
	df = pd.DataFrame({'wBrand':p_brands, 'wManufacturerId':p_manufacturerIds, 'wSupplierId':p_supplierIds, 'wSource':p_sources, 'wDescription':p_descriptions, 'wSupplementalDetails':p_details, 'wCategory':p_categories, 'wStatus':p_status})
	writer = pd.ExcelWriter(pdFile)
	df.to_excel(writer,'Product Data', index=False)
	writer.save()

	# end program
	print('Done.')

if __name__ == '__main__': main()
