from neo4j import GraphDatabase
import json
import re

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "CSE573PASS"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def clean_predicate(p):
    p = p.upper()
    p = re.sub(r'[^A-Z0-9_]', '_', p) 
    return p

def load_triples():
    with open("../Data/KnowledgeGraphData/KGRelationshipsA.json", "r", encoding="utf-8") as f:
        triples = json.load(f)

    with driver.session() as session:
        skips = 0
        for t in triples:
            try:
                subj = t["subject"].strip()
                pred = clean_predicate(t["predicate"])
                obj = t["object"].strip()

                cypher = f"""
                MERGE (s:Entity {{name: $subj}})
                MERGE (o:Entity {{name: $obj}})
                MERGE (s)-[r:{pred}]->(o)
                """
                
                session.run(cypher, subj=subj, obj=obj)
                print("Inserted:", subj, pred, obj)
            except:
                skips += 1
                print(f"Skipped. Skips: {skips}")

    print("Done Inserting Data!")

load_triples()
