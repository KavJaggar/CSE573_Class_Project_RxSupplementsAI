from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "CSE573PASS"

driver = GraphDatabase.driver(uri, auth=(user, password))

def get_relationships(tx, name):
    query = """
    MATCH (n {name: $name})-[r]-(m)
    RETURN n, r, m
    """
    return list(tx.run(query, name=name))

with driver.session() as session:
    result = session.execute_write(get_relationships, "acerola")

    for record in result:
        n = record["n"]
        r = record["r"]
        m = record["m"]

        print("Node:", n)
        print("Relationship:", r.type)
        print("To Node:", m)
        print("-----")
