# first, load constraint into the db
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'devPass'))

with driver.session() as session:
    session.run('CREATE CONSTRAINT ON (p:Product) ASSERT p.manufacturerPartNo IS UNIQUE;')

# next, load data from csv
# Category	Brand	Manufacturer_PartNo        Brammer_Web_ID	Description	     Details
# category  brand   manufacturerPartNo         brammerId     description      attributes
create_brammer_query = '''
LOAD CSV WITH HEADERS FROM "file:///Brammer Online Product Data.csv" AS bcsv
FIELDTERMINATOR '|'
WITH bcsv
WHERE bcsv.Description IS NOT NULL
MERGE(p:Product {catName: bcsv.Category, prodDescription: bcsv.Description, brand: bcsv.Brand, mnfPrtNo: bcsv.Manufacturer_PartNo, brammerId: bcsv.Brammer_Web_ID})
WITH bcsv
WHERE bcsv.Category IS NOT NULL
MERGE(c:Category {catName: bcsv.Category})
WITH bcsv
MERGE(a:Attributes {prodDescription: bcsv.Description, attributes: bcsv.Details})
// create category to product relationships (rem row by row as csv loads)
WITH bcsv
MATCH
(ca:Category {catName: bcsv.Category}),
(pr:Product {catName: bcsv.Category, prodDescription: bcsv.Description, brand: bcsv.Brand, mnfPrtNo: bcsv.Manufacturer_PartNo, brammerId: bcsv.Brammer_Web_ID}),
(at:Attributes {prodDescription: bcsv.Description, attributes: bcsv.Details})
CREATE
(ca)-[:HAS_PRODUCT]->(pr),
(pr)-[:HAS_ATTRIBUTES]->(at);
'''

with driver.session() as session:
    result = session.run(create_brammer_query)
