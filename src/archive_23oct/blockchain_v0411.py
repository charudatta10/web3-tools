import hashlib
import json
import time
import jwt
import logging
from cryptography.hazmat.primitives import serialization
from wallet import Wallet

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Block:
    def __init__(self):
        self.difficulty = 1

    def __str__(self):
        return json.dumps(self.payload)

    def mint_block(self, previous_token, public_key):
        verified_token = self.verify_jwt(previous_token, public_key)
        if not verified_token:
            return None
        del verified_token["hash"]
        previous_hash = self.compute_hash(verified_token)
        self.payload = self.proof_of_work(self.payload)
        self.token = self.create_jwt(self.payload, self.private_key)

    @staticmethod
    def create_payload(index, nonce, transactions, previous_hash):
        payload = {
            "index": index,
            "nonce": nonce,
            "transactions": transactions,
            "timestamp": time.time(),
            "previous_hash": previous_hash,
        }
        payload["hash"] = Block.compute_hash(payload)
        return payload

    @staticmethod
    def compute_hash(block):
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, payload):
        while True:
            try:
                if "hash" in payload:
                    del payload["hash"]
                    current_hash = self.compute_hash(payload)
                else:
                    current_hash = self.compute_hash(payload)
            except Exception as e:
                logging.error(f"Error is payload <{e}> {payload}")
            
            if current_hash[:self.difficulty] == "0" * self.difficulty:
                payload["hash"] = current_hash
                return payload
            payload["nonce"] += 1


    @staticmethod
    def create_jwt(payload, private_key):
        return jwt.encode(payload, private_key, algorithm="RS256")

    @staticmethod
    def verify_jwt(token, public_key):
        try:
            return jwt.decode(token, public_key, algorithms=["RS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def create_genesis_token(private_key_bytes):
        payload = {
            "index": 0,
            "nonce": 0,
            "transactions": "Genesis Block",
            "timestamp": time.time(),
            "previous_hash": "0"
        }
        payload["hash"] = Block.compute_hash(payload)
        private_key_obj = serialization.load_pem_private_key(private_key_bytes, password=None)
        token = jwt.encode(payload, private_key_obj, algorithm="RS256")
        with open("Genesis-Token.txt", "w") as f:
            f.write(token)
        return token

    @staticmethod
    def token_to_block(token, public_key):
        block_payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return block_payload


class Blockchain:
    def __init__(self, genesis_wallet):
        self.chain = []
        self.genesis_wallet = genesis_wallet
        self.wallets = {genesis_wallet.address: genesis_wallet}
        self.create_genesis_block()

    def create_genesis_block(self):
        # Serialize the private key to bytes
        private_key_bytes = self.genesis_wallet.private_key
        genesis_token = Block.create_genesis_token(private_key_bytes)
        genesis_block = Block(0, "Genesis Block", genesis_token, self.genesis_wallet)
        genesis_block.mint_block()
        self.chain.append(genesis_block.payload)

    def add_block(self, transactions, wallet):
        if wallet.address not in self.wallets:
            raise Exception("Wallet not found")
        previous_token = Block.create_jwt(self.chain[-1], wallet.private_key)
        new_block = Block(len(self.chain), transactions, previous_token, wallet)
        new_block.mint_block()
        self.chain.append(new_block.payload)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block["previous_hash"] != previous_block["hash"]:
                logging.error(f"Invalid hash at block {i}")
                return False
            if not Block.verify_jwt(Block.create_jwt(current_block, wallet.private_key), self.genesis_wallet.get_public_key_obj()):
                logging.error(f"Invalid token at block {i}")
                return False
        return True

    def add_wallet(self, wallet):
        self.wallets[wallet.address] = wallet

# Example usage
"""
genesis_wallet = Wallet()
blockchain = Blockchain(genesis_wallet)

new_wallet = Wallet()
blockchain.add_wallet(new_wallet)
print(f"0: -> {str(blockchain.chain[0])}")
blockchain.add_block("A-> B: 5", new_wallet)
print(f"1: -> {str(blockchain.chain[1])}")
blockchain.add_block("B-> A: 2", new_wallet)
print(f"2: -> {str(blockchain.chain[2])}")
print("Is the blockchain valid?", blockchain.is_chain_valid())

for block in blockchain.chain:
    print(block)
"""