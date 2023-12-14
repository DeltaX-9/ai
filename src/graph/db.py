import csv
import os
import logging
from neo4j import GraphDatabase


class GraphDB():
    def __init__(self) -> None:
        self.neo4j_uri = os.getenv("NEO4J_URI")
        self.neo4j_user = os.getenv("NEO4J_USER")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.URI = self.neo4j_uri
        self.AUTH = (self.neo4j_user,self.neo4j_password)
        self.driver:GraphDatabase.driver = self.connect_to_db(self.URI,self.AUTH)

    def connect_to_db(self,uri: str, auth: tuple) -> GraphDatabase.driver or None:
        try:
            driver = GraphDatabase.driver(uri=uri, auth=auth)
            driver.verify_connectivity()
            logging.info("Connected to the Neo4j Database")
            return driver
        
        except Exception as e:
            print(f"Error while connecting to the Neo4j Database: {e}")
            return None
    