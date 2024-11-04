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
        return "None" # json.dumps()

    def mint_block(self, index, transactions, previous_token, wallet):
        verified_token = self.verify_jwt(previous_token, wallet.get_public_key_obj())
        if not verified_token:
            return None
        del verified_token["hash"]
        previous_hash = self.compute_hash(verified_token)
        payload = self.create_payload(index, 0, transactions, previous_hash)
        payload = self.proof_of_work(payload)
        token = self.create_jwt(payload, wallet.get_private_key_obj())
        return token

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

    

class Blockchain:
    def __init__(self, genesis_wallet):
        self.chain = []
        self.create_genesis_block(genesis_wallet)

    def create_genesis_block(self, genesis_wallet):
        b1 = Block()
        genesis_token = Block.create_genesis_token(genesis_wallet.private_key)
        self.chain.append(genesis_token)

    def add_block(self, transactions, wallet):
        # check wallet if exist
        b1 = Block()
        m1 = b1.mint_block(len(self.chain), transactions, self.chain[-1], wallet)
        self.chain.append(m1)

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
        pass 

    def __str__(self):
        temp = " "
        for block in blockchain.chain:
            temp + block
        return temp

def example_block():
    genesis_wallet = Wallet()

    b1 = Block()
    genesis_token = Block.create_genesis_token(genesis_wallet.private_key)
    m1 = b1.mint_block(1, "Second Block", genesis_token, genesis_wallet)
    print(f"Minted 2nd block:{m1}\n")
    m2 = b1.mint_block(2, "Third Block", m1, genesis_wallet)
    print(f"Minted 3nd block:{m2}\n")
    m3 = b1.mint_block(3, "Fourth Block", m2, genesis_wallet)
    print(f"Minted 4nd block:{m3}\n")

    print(f" Genesis block payload: {b1.verify_jwt(genesis_token, genesis_wallet.public_key)}\n")
    print(f" 1st block payload: {b1.verify_jwt(m1, genesis_wallet.public_key)}\n")
    print(f" 2nd block payload: {b1.verify_jwt(m2, genesis_wallet.public_key)}\n")
    print(f" 3rd block payload: {b1.verify_jwt(m3, genesis_wallet.public_key)}\n")

# Example usage
if __name__ == "__main__":
    
    example_block()
    genesis_wallet = Wallet()
    blockchain = Blockchain(genesis_wallet)
    print(str(blockchain))
    #blockchain.add_wallet(new_wallet)
    #new_wallet = Wallet()
    #blockchain.add_wallet(new_wallet)
    #print(f"0: -> {str(blockchain.chain[0])}")
    blockchain.add_block("A-> B: 5", genesis_wallet)
    print(f"1: -> {blockchain.chain[1]}")
    blockchain.add_block("B-> A: 2", genesis_wallet)
    print(f"2: -> {blockchain.chain[2]}")
    #print("Is the blockchain valid?", blockchain.is_chain_valid())
    print(blockchain.chain)

    #for block in blockchain.chain:
    #    print(block)
