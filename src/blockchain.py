import hashlib
import json
import time
import jwt
import logging
from cryptography.hazmat.primitives import serialization
from src.wallet import Wallet
from src.db import insert_data, query_data, check_if_data_exists, query_metadata, insert_metadata
from src.torrent import create_torrent, download_torrent, seed_torrent
from block import Block
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class Chain:
    def __init__(self):
        self.wallet = Wallet()

    def initialize_chain(self):
        genesis_token = Block.create_genesis_token(self.wallet.private_key)
        self.add_block(0, "Genesis Block", genesis_token)
        insert_metadata("block_count", 1)  # Initialize block count

    def add_block(self, index, transactions, previous_token):
        block = Block()
        new_token = block.mint_block(index, transactions, previous_token, self.wallet)
        if new_token:
            current_count = self.get_block_count()
            insert_metadata("block_count", current_count + 1)
            return new_token
        return None

    def verify_chain(self):
        for i in range(1, self.get_block_count()):
            current_block = self.get_block(i)
            previous_block = self.get_block(i - 1)
            if current_block["previous_hash"] != previous_block["hash"]:
                return False
            if Block.compute_hash(current_block) != current_block["hash"]:
                return False
        return True

    def display_chain(self):
        for i in range(self.get_block_count()):
            block = self.get_block(i)
            if block:
                print(json.dumps(block, indent=4))

    def get_block(self, index):
        block = query_data(index)
        if block:
            return json.loads(block)

        torrent_file = f"blocks/block_{index}.torrent"
        if not check_if_data_exists(torrent_file):
            download_torrent(torrent_file)

        block_path = f"blocks/block_{index}.json"
        if os.path.exists(block_path):
            with open(block_path, "r") as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Block {index} not found in database or via torrent")

    def get_block_count(self):
        count = query_metadata("block_count")
        return int(count) if count else 0

    def query_block_by_index(self, index):
        return self.get_block(index)

    def query_block_by_transaction(self, transaction):
        results = []
        for i in range(self.get_block_count()):
            block = self.get_block(i)
            if transaction in block["transactions"]:
                results.append(block)
        return results

    def query_block_by_timestamp(self, start_time, end_time):
        results = []
        for i in range(self.get_block_count()):
            block = self.get_block(i)
            if start_time <= block["timestamp"] <= end_time:
                results.append(block)
        return results

if __name__ == "__main__":
    chain = Chain()
    chain.initialize_chain()
    previous_token = chain.get_block(0)["token"]
    
    for i in range(1, 10):
        transactions = f"A : 20 -> B {i}"
        new_token = chain.add_block(i, transactions, previous_token)
        if new_token:
            previous_token = new_token
        else:
            print(f"Block {i} minting failed")

    chain.display_chain()
    
    block_by_index = chain.query_block_by_index(3)
    print(f"Block with index 3: {json.dumps(block_by_index, indent=4)}")

    blocks_by_transaction = chain.query_block_by_transaction("A : 20 -> B 5")
    print(f"Blocks with transaction 'A : 20 -> B 5': {[json.dumps(block, indent=4) for block in blocks_by_transaction]}")

    blocks_by_timestamp = chain.query_block_by_timestamp(time.time() - 10000, time.time())
    print(f"Blocks within timestamp range: {[json.dumps(block, indent=4) for block in blocks_by_timestamp]}")
