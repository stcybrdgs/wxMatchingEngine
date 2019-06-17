  # get product group data file and feed the info into a text object
  csv_path = '../store/model/erp10/pumps/prod_pumps_erp10.csv'
  #txt_obj = '.'
  with open (csv_path) as data:
      reader = csv.reader(data, delimiter =' ', quotechar = ' ',
                          quoting = csv.QUOTE_MINIMAL)
      for row in reader:
          txt_obj = txt_obj + ' '.join(row) + '\n'

  # clean the text object
  txt_obj = preprocessor.string_cleaner(txt_obj)
  print(txt_obj)

  # create the nlp object:
  pumps_erp10 = nlp(txt_obj)

  for token in pumps_erp10:
      print(token.text)

  with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as data:
      docObj = csv.reader(data, delimiter='|')
      for row in docObj:
          print(row)

  # create model ------------------
  # get doc

  with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as infile:
      fileObj = csv.reader(infile, delimiter='|')
      doc = ''
      for row in fileObj:
          print(row)

  csv_reader = csv.DictReader(csv_file)

  data = ''
  with open('../store/model/erp10/pumps/prod_pumps_erp10.csv') as data:
      data = csv.reader(data, delimiter='|')
      headers = []
      productIDs = []
      products = []
      suppliers = []
      mpns = []
      i = 0
      for row in data:
          if i == 0:
              headers.append(row)
          else:
              productID = row[0]
              product = row[1]
              supplier = row[2]
              mpn = row[3]

              productIDs.append(productID)
              products.append(product)
              suppliers.append(supplier)
              mpns.append(mpn)
          i += 1
  print(headers)
  print(productIDs)

  print('csv_reader: \n')
  for row in csv_reader:
      print(row)
  print('headers: \n', headers)

  # clean the test string
  doc = preprocessor.string_cleaner(doc)
  print('/nstring clean doc:/n', doc)

  # create nlp object from test string
  processor.create_nlp_object(doc)