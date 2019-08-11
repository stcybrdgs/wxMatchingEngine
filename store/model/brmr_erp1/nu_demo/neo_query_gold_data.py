from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'devpass'))

with driver.session() as session:
    result = session.run('MATCH (c:Category)-[:HAS_PRODUCT]->(p:Product) WHERE c.catName = \'Bearing\' RETURN DISTINCT p.manufacturer AS Manuf')

manufs = []
for record in result:
    #print(record['Manuf'])
    manufs.append({'record':record['Manuf']})

print(manufs, '\n')

'''
'MATCH (c:Category)-[:HAS_PRODUCT]->(p:Product)-[:HAS_ATTRIBUTES]->(a:Attributes) WHERE c.catName = \'Bearing\' RETURN DISTINCT p.prodDescription AS Product, p.manufacturerId AS Manuf_Id, p.manufacturer as Manuf, a.attributes AS Attributes'
'''
