import json
from neo4j import GraphDatabase
import os
neo4j_uri = "neo4j://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "adminadmin"
URI = neo4j_uri
AUTH = (neo4j_user,neo4j_password)

## WALLET ----SENT----> TRANSACTION ---OUTPUT----> WALLET

def connect_to_db(uri: str, auth: tuple) -> GraphDatabase.driver or None:
    try:
        driver = GraphDatabase.driver(uri=uri, auth=auth)
        driver.verify_connectivity()
        return driver
    
    except Exception as e:
        print(f"Error while connecting to the Neo4j Database: {e}")
        return None
    



driver = connect_to_db(URI,AUTH)
data_file_path = os.path.join(os.path.dirname(__file__), 'data.json')
data_file = open(data_file_path, 'r')
data = json.load(data_file)





def create_transaction_node(driver,data):
    transaction_data = data['transaction']
    inputs = data['inputs']
    outputs = data['outputs']
    records, summary, keys = driver.execute_query(
        "MERGE (transaction:Transaction {transaction_id: $transaction_id}) "
        "SET transaction += $props ",
        transaction_id=transaction_data["hash"], 
        props=transaction_data,
        database_="neo4j"
    )

    print(keys)

    ## Create Input Wallet Nodes
    for input_address in inputs:
        records, summary, keys = driver.execute_query(
            "MATCH (transaction:Transaction {transaction_id: $transaction_id })"
            "MERGE (wallet:Wallet {wallet_id: $wallet_id}) "
            "MERGE (wallet)-[sent:SENT {relation_id: $relation_id}]->(transaction) "
            "SET sent += $relation_props",
            wallet_id=input_address["recipient"],
            relation_id=f"{input_address['spending_index']}_{input_address['spending_transaction_hash']}",
            transaction_id=input_address["spending_transaction_hash"], 
            relation_props=input_address,
            database_="neo4j"
        )
        print(records)

    
    ## Create Output Wallet Nodes
    for output_address in outputs:
        records, summary, keys = driver.execute_query(
            "MATCH (transaction:Transaction {transaction_id: $transaction_id })"
            "MERGE (wallet:Wallet {wallet_id: $wallet_id}) "
            "MERGE (wallet)<-[received:RECEIVED {relation_id: $relation_id}]-(transaction) "
            "SET received += $relation_props",
            wallet_id=output_address["recipient"],
            relation_id=f"{output_address['index']}_{output_address['spending_transaction_hash']}",
            transaction_id=output_address["transaction_hash"], 
            relation_props=output_address,
            database_="neo4j"
        )
        print(records)
    

    
    

    


create_transaction_node(driver,data['e8b406091959700dbffcff30a60b190133721e5c39e89bb5fe23c5a554ab05ea'])