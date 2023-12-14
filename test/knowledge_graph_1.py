##Test - 1 
##Insertion operation on Graph Database
import csv
from neo4j import GraphDatabase
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
    

def insert_data(data,driver) : 
    records, summary, keys = driver.execute_query(
        "MERGE (sender:Wallet {wallet_id: $sender_wallet}) "
        "MERGE (receiver:Wallet {wallet_id: $receiver_wallet}) "

        "MERGE (transaction:Transaction {transaction_id: $transaction_id}) "
        "ON CREATE SET transaction.amount = toFloat($amount) "
        "ON MATCH SET transaction.amount = transaction.amount + toFloat($amount) "


        "MERGE (sender)-[:SENT {amount: toFloat($amount)} ]->(transaction) "
        "MERGE (transaction)-[:RECEIVED {amount: toFloat($amount)}]->(receiver)",
        sender_wallet=data["sender_wallet"], 
        receiver_wallet=data["receiver_wallet"], 
        transaction_id=data["transaction_id"], 
        amount=data["amount"],
        # timestamp=data["timestamp"] + "T00:00:00",
        database_="neo4j"
    )

     # Get the result
    

    ## Print the result
    for record in records:
        print(record["name"])
        print(record["name"])
 
    
    print(summary.counters)
    print(summary.query)



test_dataset = open("./test.csv","r")
test_csv = csv.DictReader(test_dataset)
driver = connect_to_db(URI,AUTH)
for x in (test_csv):
    insert_data(x,driver)
    # print(x)
    