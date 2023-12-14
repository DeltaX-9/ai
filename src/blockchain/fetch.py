import requests
import os

class BlockChainDataFetch():
    def __init__(self) -> None:
        self.baseURL = f"{os.getenv('BACKEND_API_URL')}"
        self.transactionRoute = "/blockchain/transaction"
        self.addressRoute = "/blockchain/address"

    def get_transaction_data(self, tx_hash, btc_chain) -> dict:
        url = f"{self.baseURL}{self.transactionRoute}/{tx_hash}?btc_chain={btc_chain}"
        response = requests.get(url)
        return response.json()
    
    def get_address_data(self, address, btc_chain):
        url = f"{self.baseURL}{self.addressRoute}/{address}?btc_chain={btc_chain}"
        response = requests.get(url)
        return response.json()