import requests
import csv

# set api-endpoint for local flask rest api
URL = "http://127.0.0.1:5000/product/"

inFile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\nu_demo\out_mmat_pandas.csv'
manuf_ids = []
with open(inFile) as data:
    csv_reader = csv.reader(data, delimiter='|')
    i = 0
    for row in csv_reader:
        if i > 0:
            id = row[0]
            manuf_ids.append(id)
            # populate txt obj
            #doc = doc + 'wrwx ' + ('|'.join(row) + '\n')
        i += 1

for manuf_id in manuf_ids:
    # send get request and save response as response object
    #PARAMS = 'Stacy'
    r = requests.get(url = URL + manuf_id)  #, params = PARAMS)

    # extracting data in json format
    data = r.json()

    # Product	Manuf_Id	Manuf	Attributes
    try:
        product = data['product']
    except:
        product = 'none'
    try:
        manuf_id = data['manuf_id']
    except:
        manuf_id = 'none'
    try:
        manuf = data['manuf']
    except:
        manuf = 'none'
    try:
        attributes = data['attributes']
    except:
        attributes = 'none'

    if manuf_id == 'none':
        print('Product not found')
    else:
        print('Product: {}, Manuf: {}, Manuf_Id: {}, Attributes: {}'.format(product, manuf, manuf_id, attributes))
