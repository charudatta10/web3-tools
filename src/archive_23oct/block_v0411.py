import hashlib
import json
import time
import jwt
import logging
from cryptography.hazmat.primitives import serialization

class Block:
    def __init__(self, index, transactions, previous_token, wallet):
        self.private_key = wallet.get_private_key_obj()
        self.public_key = wallet.get_public_key_obj()
        self.difficulty = 1
        self.payload = self.create_payload(index, 0, transactions, previous_token, self.public_key)
        self.token = None

    def mint_block(self):
        self.payload = self.proof_of_work(self.payload)
        self.token = self.create_jwt(self.payload, self.private_key)

    def create_payload(self, index, nonce, transactions, previous_token, public_key):
        verified_token = self.verify_jwt(previous_token, public_key)
        if not verified_token:
            return None
        del verified_token["hash"]
        previous_hash = self.compute_hash(verified_token)
        payload = {
            "index": index,
            "nonce": nonce,
            "transactions": transactions,
            "timestamp": time.time(),
            "previous_hash": previous_hash
        }
        payload["hash"] = self.compute_hash(payload)
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

    def create_jwt(self, payload, private_key):
        return jwt.encode(payload, private_key, algorithm="RS256")

    def verify_jwt(self, token, public_key):
        try:
            return jwt.decode(token, public_key, algorithms=["RS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def create_genesis_token(private_key):
        payload = {
            "index": 0,
            "nonce": 0,
            "transactions": "Genesis Block",
            "timestamp": time.time(),
            "previous_hash": "0"
        }
        payload["hash"] = Block.compute_hash(payload)
        token = jwt.encode(payload, private_key, algorithm="RS256")
        with open("Genesis-Token.txt", "w") as f:
            f.write(token)
        return token

    @staticmethod
    def token_to_block(token, wallet):
        public_key = wallet.get_public_key_obj()
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        block = Block(decoded['index'], decoded['transactions'], decoded['previous_hash'], wallet)
        block.payload = decoded
        block.token = token
        return block

    def block_to_token(self):
        return self.token
