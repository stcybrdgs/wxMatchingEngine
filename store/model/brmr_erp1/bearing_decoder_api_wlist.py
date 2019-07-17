# -*- coding: utf-8 -*-
'''
Wenesday July 17, 2019
Stacy Bridges

bearing decoder
- this script makes GET request from SKF API using mMatIDs

mMat  |  shortDescription  |  longDescription  |  Attributes[]

'''
# IMPORTS  ---------------------------------------------------------
import csv
import requests

# GLOBALS  ---------------------------------------------------------
row_heads = []
mMats = []

# FUNCTIONS  -------------------------------------------------------
def import_csv(d):
	global row_heads
	row_heads.clear()
	doc = ''
	code = ''
	with open(d) as data:
		csv_reader = csv.reader(data, delimiter='|')
		i = 0
		for row in csv_reader:
			if i == 0:
				row_head = row[0]
				row_heads.append(row_head)
			elif i > 0:
				# populate txt obj
				doc = doc + ('|'.join(row) + '\n')
				code = row
				mMats.append(code)
			i += 1
	return doc
    # end function //

# MAIN  ------------------------------------------------------------
def main():
	descriptions = []
	attributes = []
	input_file = 'bearing_decoder_input.csv'

	# get codes as doc obj from external file
	codes = import_csv(input_file)

	# set api-endpoint for SKF
	URL = "https://search.skf.com/prod/search-skfcom/rest/apps/site_search/searchers/products"

	with open('bearing_decoder_output.csv', 'w') as writeFile:
		writer = csv.writer(writeFile)

		i = 0
		for code in mMats:
			# sending get request and saving the response as response object
			PARAMS = {'q':code}
			r = requests.get(url = URL, params = PARAMS)

			# extracting data in json format
			data = r.json()

			# get description (ie, designation and category)
			designation = data['documentList']['documents'][0]['designation']
			category = data['documentList']['documents'][0]['category']
			descriptions.append([designation, category])

			print(designation, '|', end='')
			print(category, '|', end='')

			# get attributes
			search_result = data['documentList']['documents'][0]['search_result_nested']
			j = 0
			for item in search_result:
				attributes.append({
					search_result[j]['name'],
					search_result[j]['value'],
					search_result[j]['unit']
				})
				print({
					search_result[j]['name'],
					search_result[j]['value'],
					search_result[j]['unit']
				}, end='')
				j += 1
			print('')

		'''
		with open('bearing_decoder_output.csv', 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows()
		'''

	# end program
	print('Done.')

if __name__ == '__main__': main()
