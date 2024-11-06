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