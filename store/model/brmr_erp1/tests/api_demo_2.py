# build an api caller
import requests
import pandas as pd
from pandas import ExcelWriter
import numpy

# create parameters
url = 'https://api.ince.live/product'  # url
apikey = '4f032b1a18ab3f36'  # apikey
id = '6001'  # id
params = {'apikey': apikey , 'id': id}

# create request object
r = requests.get(url, params)
print(r)

# parse request object
data = r.json()
print(data)

# get index
# brand | mpn | description
brands = []
mpns = []
descs = []
i = 0
for item in data:
    #print(item['brand'])
    #print(data[i]['brand'])
    brands.append(item['brand'])
    mpns.append(item['manufacturerID'])
    descs.append(item['description'])
    print(brands[i], mpns[i], descs[i])
    i += 1

# write to excel file - UPDATE FOR YOUR LOCAL MACHINE
outfile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\tests\api_demo_2_out.xlsx'

# create data frame
df = pd.DataFrame({
    'Brands': brands,
    'MPNs': mpns,
    'Descriptions': descs
})

# create writer
writer = pd.ExcelWriter(outfile)

# write to file
df.to_excel(writer, 'API Results', index=False)

# save
writer.save()

# end program
print('Done.')
