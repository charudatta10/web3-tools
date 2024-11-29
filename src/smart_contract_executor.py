import json
import os
import hashlib
import time
import logging
import jwt
from cryptography.hazmat.primitives import serialization
from wallet import Wallet
from block import Block
from cryptoleq import Cryptoleq
from torrent_blockchain import TorrentBlockchain

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmartContractExecutor:
    def __init__(self, N):
        self.cryptoleq = Cryptoleq(N)
        self.blockchain = TorrentBlockchain()
        self.wallet = self.blockchain.wallet

    def load_smart_contract(self, filename):
        with open(filename, 'r') as f:
            smart_contract = json.load(f)
        return smart_contract

    def execute_smart_contract(self, smart_contract):
        for instruction in smart_contract:
            a = instruction['a']
            b = instruction['b']
            c = instruction['c']
            self.cryptoleq.memory = instruction['memory']
            self.cryptoleq.IP = instruction['IP']
            self.cryptoleq.execute()
            logging.info(f"Executed instruction: {instruction}")

            # Create a JWT block for the executed instruction
            payload = {
                'a': a,
                'b': b,
                'c': c,
                'IP': self.cryptoleq.IP,
                'memory': self.cryptoleq.memory,
                'timestamp': time.time()
            }
            token = self.create_jwt(payload)
            logging.info(f"Created JWT: {token}")

            # Share the block using torrents
            torrent_file = self.blockchain.share_block(token, f'block_{self.cryptoleq.IP}.json')
            logging.info(f"Shared block: {torrent_file}")

    def create_jwt(self, payload):
        private_key = self.wallet.get_private_key_obj()
        return jwt.encode(payload, private_key, algorithm='RS256')

# Example usage
if __name__ == '__main__':
    executor = SmartContractExecutor(N=10)
    
    # Load and execute a smart contract
    smart_contract = executor.load_smart_contract('smart_contract.json')
    executor.execute_smart_contract(smart_contract)
