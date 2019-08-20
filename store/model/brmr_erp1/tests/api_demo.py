# import requests module
import requests
import pandas as pd
import numpy as np
from pandas import ExcelWriter

# identify url
url = 'https://api.ince.live/product'

# identify api request arguments
apikey = '4f032b1a18ab3f36'
id = '6001'
params = {'apikey': apikey, 'id': id}

# make a request object
r = requests.get(url, params)
print(r)

# parse response into a data object
data = r.json()
print(data)

i = 0
for item in data:
    print(data[i])
    i += 1

# brand | manufacturerID | description
brands = []
manufacturerIDs = []
descriptions = []
i = 0
for item in data:
    brands.append(data[0]['brand'])
    manufacturerIDs.append(data[0]['manufacturerID'])
    descriptions.append(data[0]['description'])
    i += 1

i = 0
for item in brands:
    print(brands[i], manufacturerIDs[i], descriptions[i])
    i += 1

# write api results to excel file
outfile = r'C:\Users\stacy\My GitHub\wxMatchingEngine\store\model\brmr_erp1\tests\api_demo_out.xlsx'

# create data frame
df = pd.DataFrame({'Brands': brands, 'MPNs': manufacturerIDs , 'Descriptions': descriptions})

# create data writer
writer = pd.ExcelWriter(outfile)

# write to excel
df.to_excel(writer,'API Results', index=False)

# save
writer.save()

# end program
print('Done.')
