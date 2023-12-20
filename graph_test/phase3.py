import os
import json
from neo4j import GraphDatabase

neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "adminadmin"
URI = neo4j_uri
AUTH = (neo4j_user, neo4j_password)

def connect_to_db(uri: str, auth: tuple) -> GraphDatabase.driver or None:
    try:
        driver = GraphDatabase.driver(uri=uri, auth=auth)
        driver.verify_connectivity()
        return driver
    except Exception as e:
        print(f"Error while connecting to the Neo4j Database: {e}")
        return None

driver = connect_to_db(URI, AUTH)

# Load threat actor data
threat_actor_file_path = os.path.join(os.path.dirname(__file__), 'threat_actor_data.json')
threat_actor_file = open(threat_actor_file_path, 'r')
threat_actor_data = json.load(threat_actor_file)

# Load profile node data
profile_node_file_path = os.path.join(os.path.dirname(__file__), 'profile_node_data.json')
profile_node_file = open(profile_node_file_path, 'r')
profile_node_data = json.load(profile_node_file)

# Load bitcoin node data
bitcoin_node_file_path = os.path.join(os.path.dirname(__file__), 'bitcoin_threat_rel.json')
bitcoin_node_file = open(bitcoin_node_file_path, 'r')
bitcoin_node_data = json.load(bitcoin_node_file)

# Load wallet node data
wallet_node_file_path = os.path.join(os.path.dirname(__file__), 'bitcoin_threat_rel.json')
wallet_node_file = open(wallet_node_file_path, 'r')
wallet_node_data = json.load(wallet_node_file)

def create_threat_actor_nodes(driver, threat_actor_data):
    for document in threat_actor_data['documents']:
        # Extract primitive types from the nested map
        threat_id = document['id']
        ncat=[]
        cat=[]
        con=[]
        data=[]
        ts=[]
        for i in document['activities']:
            for j in i["category"]:
                cat.append(j)
            ncat.append(len(i["category"]))
            con.append(i["content"])
            data.append(i["data"])
            ts.append(i["timestamp"])
        props = {
            "name": document['name'],
            "number_of_categories":ncat,
            "categories": cat,
            "contents":con,
            "datas":data,
            "timestamps":ts,
            "description": document['description'],
            "target_url": document['target_url'],
            "references": document['references'],
            "tags": document['tags'],
            "type": document['type']
        }
        
        records, summary, keys = driver.execute_query(
            "MERGE (threat:Threat {id: $threat_id}) "
            "SET threat += $props",
            threat_id=threat_id,
            props=props,
            database_="neo4j"
        )
        print("create_Actor_threat_node",keys)


def create_profile_nodes(driver, profile_node_data):
    for profile_node in [profile_node_data]:
        id_key=[]
        id_v=[]
        for i in profile_node["_id"]:
            id_key.append(i)
            id_v.append(profile_node["_id"][i])
        profile_node["id_key"]=id_key
        profile_node["id_value"]=id_v
        del profile_node["_id"]
        records, summary, keys = driver.execute_query(
            "MERGE (profile:Profile {uid: $uid}) "
            "SET profile += $props",
            uid=profile_node['uid'],
            props=profile_node,
            database_="neo4j"
        )
        print(keys)

def create_activity_relationships(driver, profile_node_data):
    for threat_id in profile_node_data['threat_actor']:
        records, summary, keys = driver.execute_query(
            "MATCH (threat:Threat {id: $threat_id})"
            "MATCH (profile:Profile {uid: $profile_uid}) "
            "MERGE (threat)-[:ACTIVITY]->(profile)",
            threat_id=threat_id,
            profile_uid=profile_node_data['uid'],
            database_="neo4j"
        )
        print(records)


def create_bitcoin_node_actor(driver, document):
    # Extract primitive types from the nested map
    bitcoin_id = document['id']
    ncat=[]
    cat=[]
    con=[]
    data=[]
    ts=[]
    for i in document['activities']:
        for j in i["category"]:
            cat.append(j)
        ncat.append(len(i["category"]))
        con.append(i["content"])
        data.append(i["data"])
        ts.append(i["timestamp"])
    props = {
        "name": document['name'],
        "number_of_categories":ncat,
        "categories": cat,
        "contents":con,
        "datas":data,
        "timestamps":ts,
        "description": document['description'],
        "target_url": document['target_url'],
        "references": document['references'],
        "tags": document['tags'],
        "type": document['type']
    }
    
    records, summary, keys = driver.execute_query(
        "MERGE (bitcoin:Bitcoin {id: $bitcoin_id}) "
        "SET bitcoin += $props",
        bitcoin_id=bitcoin_id,
        props=props,
        database_="neo4j"
    )
    print("create_Actor_threat_node",keys)

# Create Threat Actor Nodes
def create_activity_relationships(driver, wallet_node_data):
    for threat_id in profile_node_data['threat_actor']:
        records, summary, keys = driver.execute_query(
            "MATCH (threat:Threat {id: $threat_id})"
            "MATCH (profile:Profile {uid: $profile_uid}) "
            "MERGE (threat)-[:ACTIVITY]->(profile)",
            threat_id=threat_id,
            profile_uid=profile_node_data['uid'],
            database_="neo4j"
        )
        print(records)

# Create Threat Actor Nodes
create_threat_actor_nodes(driver, threat_actor_data)

# Create Profile Nodes
create_profile_nodes(driver, profile_node_data)

# Create Activity Relationships
create_activity_relationships(driver, profile_node_data)

create_bitcoin_node_actor(driver, bitcoin_node_data[0])


