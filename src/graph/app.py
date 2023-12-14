from flask import current_app
from neo4j import GraphDatabase
from src.blockchain.fetch import BlockChainDataFetch
import logging


class GraphManger():
    def __init__(self ,graph_driver, blockchain_data_fetcher) -> None:
        self.graph_driver:GraphDatabase.driver = graph_driver
        self.blockchain_data_fetcher:BlockChainDataFetch = blockchain_data_fetcher

    def create_graph(self,driver,data):
        try:
            transaction_data = data['transaction']
            inputs = data['inputs']
            outputs = data['outputs']

            ## Create Transaction Node
            records, summary, keys = driver.execute_query(
                "MERGE (transaction:Transaction {transaction_id: $transaction_id}) "
                "SET transaction += $props ",
                transaction_id=transaction_data["hash"], 
                props=transaction_data,
                database_="neo4j"
            )

            logging.info(summary)

            ## Create Input Wallet Nodes && (Wallet -> Transaction) Edges
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
                logging.info(summary)

            
            ## Create Output Wallet Nodes && (Transaction -> Wallet) Edges
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
                logging.info(summary)

            return True

        except Exception as e:
            logging.error(f"Error while creating graph: {e}")

    

    def create_transaction_node(self,tx_hash, btc_chain):
        driver = self.graph_driver
        data = self.blockchain_data_fetcher.get_transaction_data(tx_hash, btc_chain)
        if not data:
            return "Error", 400
        
        if self.create_graph(driver,data):
            return "Success",200