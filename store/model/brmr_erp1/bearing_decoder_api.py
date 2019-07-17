# -*- coding: utf-8 -*-
'''
Wenesday July 17, 2019
Stacy Bridges

bearing decoder
- this script makes GET request from SKF API using

'''
# IMPORTS  ---------------------------------------------------------
import requests

# MAIN  ------------------------------------------------------------
def main():
	# api-endpoint
	URL = "https://search.skf.com/prod/search-skfcom/rest/apps/site_search/searchers/products"

	# defining a params dict for the parameters to be sent to the API
	mMat = 'NNF5005'
	PARAMS = {'q':mMat}

	# sending get request and saving the response as response object
	r = requests.get(url = URL, params = PARAMS)

	# extracting data in json format
	data = r.json()

	# get description
	description = []
	designation = data['documentList']['documents'][0]['designation']
	category = data['documentList']['documents'][0]['category']
	description.append([designation, category])

	# get attributes
	attributes = []
	search_result = data['documentList']['documents'][0]['search_result_nested']
	i = 0
	for item in search_result:
		attributes.append([
			search_result[i]['name'],
			search_result[i]['value'],
			search_result[i]['unit']
			])
		i += 1

	# printing the output
	print('search_results --------------------')
	print(description)
	print(attributes)

	# end program
	print('Done.')

if __name__ == '__main__': main()
