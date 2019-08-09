import requests

# set api-endpoint for local flask rest api
URL = "http://127.0.0.1:5000/user/"

names = ['Stacy', 'Anushree', 'Betty', 'Eric', 'Ron']

for name in names:
    # send get request and save response as response object
    #PARAMS = 'Stacy'
    r = requests.get(url = URL + name)#, params = PARAMS)

    # extracting data in json format
    data = r.json()

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
        print('User not found')
    else:
        print('Name: {}, Role: {}, Age: {}'.format(name, role, age))
