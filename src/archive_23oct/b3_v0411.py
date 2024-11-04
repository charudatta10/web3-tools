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
        return json.dumps(self.payload, indent=4) if hasattr(self, 'payload') else 'Un-minted Block'

    def mint_block(self, index, transactions, previous_token, wallet):
        verified_token = self.verify_jwt(previous_token, wallet.get_public_key_obj())
        if not verified_token:
            return None
        del verified_token["hash"]
        previous_hash = self.compute_hash(verified_token)
        payload = self.create_payload(index, 0, transactions, previous_hash)
        payload = self.proof_of_work(payload)
        token = self.create_jwt(payload, wallet.get_private_key_obj())
        self.payload = payload
        self.token = token
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
            current_hash = self.compute_hash({k: v for k, v in payload.items() if k != "hash"})
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
