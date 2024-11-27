import hashlib
import json
import time
import jwt
import logging
from cryptography.hazmat.primitives import serialization
from wallet import Wallet
from block import Block

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Blockchain:
    def __init__(self, genesis_wallet):
        self.chain = []
        self.genesis_wallet = genesis_wallet
        self.block = Block()
        self.create_genesis_block(genesis_wallet)

    def create_genesis_block(self, genesis_wallet):
        self.chain.append(Block.create_genesis_token(genesis_wallet.private_key))

    def add_block(self, transactions, wallet):
        self.chain.append(self.block.mint_block(len(self.chain), transactions, self.chain[-1], wallet))

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block_token = self.chain[i]
            current_block = Block.verify_jwt(current_block_token, self.genesis_wallet.get_public_key_obj())
            previous_block_token = self.chain[i - 1]
            previous_block = Block.verify_jwt(previous_block_token, self.genesis_wallet.get_public_key_obj())
            if current_block["previous_hash"] != previous_block["hash"]:
                logging.error(f"Invalid hash at block {i}")
                return False
            if not Block.verify_jwt(current_block_token, self.genesis_wallet.get_public_key_obj()):
                logging.error(f"Invalid token at block {i}")
                return False
        return True

    def __str__(self):
        return json.dumps([Block.verify_jwt(token, self.genesis_wallet.get_public_key_obj()).__str__() for token in self.chain], indent=4)


# Example usage
if __name__ == "__main__":

    genesis_wallet = Wallet()
    blockchain = Blockchain(genesis_wallet)
    blockchain.add_block("A-> B: 5", genesis_wallet)
    blockchain.add_block("B-> A: 2", genesis_wallet)
    print("Is the blockchain valid?", blockchain.is_chain_valid())
    print(str(blockchain))
