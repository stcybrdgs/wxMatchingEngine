#:len(d)
  #doc = loader.load_doc(d)

  '''
  # test import_txt
  #doc = ''
  with open(d) as infile:
      for line in infile:
          doc = doc + re.sub(r'^\s+$', '', line) # regex removes blank line

    doc = ''
    with open(d) as data:
        csv_readereader = csv.reader(data, delimiter='|')
        for row in csv_reader:
            doc = doc + ('|'.join(row) + '\n')

    d = ''
    with open(f_txt) as data:
        doc = csv.reader(data, delimiter='|')
        i = 0
        for row in doc:
            d = d + ('|'.join(row) + '\n')

    '''
