import hashlib
import json
import time
import jwt
import os
from block import Block


class Blockchain:
    def __init__(self, genesis_token, key):
        self.chain = []
        self.key = key
        self.genesis_token = genesis_token
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "Genesis Block", self.genesis_token, self.key)
        genesis_block.mint_block()
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        previous_token = self.chain[-1].token
        new_block = Block(len(self.chain), transactions, previous_token, self.key)
        new_block.mint_block()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verify the current block's hash
            if current_block.payload["previous_hash"] != previous_block.payload["hash"]:
                print(f"Invalid hash at block {i}")
                return False

            # Verify the current block's token
            if not current_block.verify_jwt(current_block.token, self.key):
                print(f"Invalid token at block {i}")
                return False

        return True


# Example usage
SECRET_KEY = os.getenv("BLOCK_SECRET_KEY")
with open("Genesis-Token.txt", "r") as file:
    genesis_token = file.read()

# Create the blockchain with the genesis block
blockchain = Blockchain(genesis_token, SECRET_KEY)

# Add blocks to the blockchain
blockchain.add_block("A-> B: 5")
blockchain.add_block("B-> A: 2")

# Check if the blockchain is valid
print("Is the blockchain valid?", blockchain.is_chain_valid())

# Print the blockchain
for block in blockchain.chain:
    print(block.payload)
