# -*- coding: utf-8 -*-
'''
Monday, August 12, 2019
Stacy Bridges

- this script makes GET request from ince's backend (brammer, rs)

mMat  |  shortDescription  |  longDescription  |  Attributes[]
https://api.ince.live/product?apikey=4f032b1a18ab3f36&id=6001&brand=skf

'''
# IMPORTS  ---------------------------------------------------------
import csv
import requests

# GLOBALS  ---------------------------------------------------------

mMats = []  #'6001']  #['1601', '6001', '607', '3313']

# FUNCTIONS  -------------------------------------------------------
def import_csv(d):
	doc = ''
	code = ''
	with open(d) as data:
		csv_reader = csv.reader(data, delimiter='|')
		i = 0
		for row in csv_reader:
			if i > 0:
				# populate txt obj
				doc = doc + ('|'.join(row) + '\n')
				code = row
				mMats.append(code)
			i += 1
	return doc
    # end function //


# MAIN  ------------------------------------------------------------
def main():
	# declare input/output files
	inFile = r'C:/Users/stacy/My GitHub/wxMatchingEngine/store/model/brmr_erp1/nu_demo/api_rs_component_id.csv'
	outFile = ''

	# import mmat file and populate mmats[]
	import_csv(inFile)

	# set api-endpoint for SKF
	URL = "https://api.ince.live/product"
	apikey = '4f032b1a18ab3f36'
	brand = ''

	i = 0
	for code in mMats:
		# sending get request and saving the response as response object
		if len(code) == 0:
			row_str = 'not found'
		else:
			PARAMS = {'apikey':apikey, 'id':code, 'brand':brand}
			r = requests.get(url = URL, params = PARAMS)

			# extracting data in json format
			data = r.json()

			# id: brammer id					# source: brammer
			# supplierID: supplier id			# brand: brand
			# manufacturerID: manufacturer id	# searchID: ibid
			# description: product description	# details: details
			# productCategory: bearings, etc

			try:
				manufacturerId = data['manufacturerID']
			except:
				manufacturerId = 'not found'
			try:
				category = data['productCategory']
			except:
				category = 'not found'
			try:
				brand = data['brand']
			except:
				brand = 'not found'
			try:
				description = data['description']
			except:
				description = 'not found'

			# add them to the csv string
			#row_str = row_str + designation + '|' + category + '|'

			'''
				if j > 0:
					attr_str = attr_str + ', '
				attr_str = attr_str + name + ': ' + str(value) + ' ' + unit
				j += 1

			# add the attributes to the csv string
			row_str = row_str + attr_str
			'''
		print('Pass {}: {}, {}, {}, {}'.format(i,manufacturerId, category, brand, description))

		# store the string in a list so that it can be added to the csv
		#rows_for_csv.append([row_str])

		# reset strings
		#row_str = ''
		#attr_str = ''
		#exception = False
		'''
		counter += 1
		if counter == 500:
			# write data to csv file
			writer.writerows(rows_for_csv)
			counter = 0
			rows_for_csv.clear()
		'''
		i+= 1

	# write data to csv file
	#writer.writerows(rows_for_csv)

	# end program
	print('Done.')

if __name__ == '__main__': main()
