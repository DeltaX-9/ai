import json
from neo4j import GraphDatabase
import os
neo4j_uri = "neo4j://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "adminadmin"
URI = neo4j_uri
AUTH = (neo4j_user,neo4j_password)



def connect_to_db(uri: str, auth: tuple) -> GraphDatabase.driver or None:
    try:
        driver = GraphDatabase.driver(uri=uri, auth=auth)
        driver.verify_connectivity()
        return driver
    
    except Exception as e:
        print(f"Error while connecting to the Neo4j Database: {e}")
        return None
    
driver = connect_to_db(URI,AUTH)
data_file_path = os.path.join(os.path.dirname(__file__), 'neo4j.json')
data_file = open(data_file_path, 'r')
data = json.load(data_file)

def create_actor(driver,data):
    records, summary, keys = driver.execute_query(
        "MERGE (actor:Actor {id: $id})",
        "MERGE (url:URL {id: $url_id})",
        "MERGE (actor)-[:CONTAINS]->(url)",
        id=data["id"], 
        url_id=data["target_url"],
        # props=data,
        database_="neo4j"
    )

    print(keys)
    


for x in data:
    create_actor(driver,x)