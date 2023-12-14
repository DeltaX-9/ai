import dotenv
dotenv.load_dotenv()
from flask import Flask, request
import logging
from src.blockchain.fetch import BlockChainDataFetch
from src.graph.db import GraphDB
from src.graph.app import GraphManger

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)
blockchain_data_fetcher = BlockChainDataFetch()
graph_driver = GraphDB().driver
graph_creator = GraphManger(graph_driver, blockchain_data_fetcher)


@app.route('/graph/transaction', methods=['POST'])
def graph_transaction():
    data = request.get_json()
    btc_chain = data['btc_chain']
    tx_hash = data['tx_hash']
    ## if btc_chain or tx_hash is not provided, return error
    if not btc_chain or not tx_hash:
        return "Error", 400
    
    return graph_creator.create_transaction_node(tx_hash, btc_chain)


if __name__ == '__main__':
    app.run(debug=True,port=5116)
