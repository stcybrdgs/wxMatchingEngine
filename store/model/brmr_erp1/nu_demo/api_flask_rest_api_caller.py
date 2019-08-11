import requests

# set api-endpoint for local flask rest api
URL = "http://127.0.0.1:5000/product/"

names = ['Stacy', 'Anushree', 'Betty', 'Eric', 'Ron', '3313', '7205 BEGAP', '16016', '607']

for name in names:
    # send get request and save response as response object
    #PARAMS = 'Stacy'
    r = requests.get(url = URL + name)#, params = PARAMS)

    # extracting data in json format
    data = r.json()

    # Product	Manuf_Id	Manuf	Attributes
    try:
        name = data['name']
    except:
        name = 'none'
    try:
        role = data['role']
    except:
        role = 'none'
    try:
        age = data['age']
    except:
        age = 'none'

    if name == 'none':
        print('Product not found')
    else:
        print('Name: {}, Role: {}, Age: {}'.format(name, role, age))
