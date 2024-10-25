import hashlib
import json
import time
import jwt
import os

class Block:
    def __init__(self, index, transactions, previous_token, key):
        self.key = key
        self.difficulty = 1
        self.payload = self.create_payload(index, 0, transactions, previous_token, key)
        self.token = None

    def mint_block(self):
        self.payload = self.proof_of_work(self.payload)
        self.token = self.create_jwt(self.payload, self.key)

    def create_payload(self, index, nonce, transactions, previous_token, key):
        verified_token = self.verify_jwt(previous_token, key)
        if not verified_token:
            return None
        del verified_token['hash']
        previous_hash = self.compute_hash(verified_token)
        payload = {
            "index": index,
            "nonce": nonce,
            "transactions": transactions,
            "timestamp": time.time(),
            "previous_hash": previous_hash,
        }
        payload["hash"] = self.compute_hash(payload)
        return payload

    def compute_hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, payload):
        while True:
            current_hash = self.compute_hash({k: v for k, v in payload.items() if k != "hash"})
            if current_hash[:self.difficulty] == "0" * self.difficulty:
                payload["hash"] = current_hash
                return payload
            payload["nonce"] += 1

    def create_jwt(self, payload, key):
        return jwt.encode(payload, key, algorithm="HS256")

    def verify_jwt(self, token, key):
        try:
            return jwt.decode(token, key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token")
            return None

# Example usage
SECRET_KEY = os.getenv('BLOCK_SECRET_KEY')
with open("Genesis-Token.txt", 'r') as file:
    genesis_token = file.read()

b1 = Block(1, "A-> B: 2", genesis_token, SECRET_KEY)
b1.mint_block()
print(b1.payload)

b2 = Block(2, "B-> A: 2", b1.token, SECRET_KEY)
b2.mint_block()
print(b2.payload)
