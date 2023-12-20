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
    

def create_node(driver,data):
    for x in (data):
        records, summary, keys = driver.execute_query(
        "MERGE (transaction:Transaction {transaction_id: $transaction_id}) "
        "SET transaction += $props ",
        transaction_id=transaction_data["hash"], 
        props=transaction_data,
        database_="neo4j"
    )



    



driver = connect_to_db(URI,AUTH)
data_file_path = os.path.join(os.path.dirname(__file__), 'data2.json')
data_file = open(data_file_path, 'r')
data = json.load(data_file)

create_node(driver,data)