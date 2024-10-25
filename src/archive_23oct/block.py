from datetime import datetime
from uuid import uuid4
import base64
import json

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from src.wallet import Wallet
from src.transaction import Transaction


class Block:
    def __init__(self, data, prev_data, transactions, *args) -> None:
        private_key, public_key = self._get_keys(*args)
        self.id = str(uuid4())
        self.time = str(datetime.now())
        self.height = prev_data.height + 1 if prev_data else 0
        self.difficulty = self.calculate_difficulty()
        self.version = "1.0"
        self.data = data
        self.transactions = transactions
        self.tx_count = len(transactions)
        self.merkle_root = self.calculate_merkle_root(transactions)
        self.link = (
            self._get_hash(json.dumps(prev_data.get_dict())) if prev_data else ""
        )
        self.author = self._key_conversion(public_key)
        self.nonce = self.proof_of_work(1)
        self.sign = self.get_sign(
            self.id + self.nonce + self.time + self.data + self.link + self.author,
            private_key,
        )

    def _get_keys(self, private_key_path, public_key_path):
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None, backend=default_backend()
            )

        with open(public_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(), backend=default_backend()
            )
        return private_key, public_key

    def _get_hash(self, data: str) -> str:
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data.encode("utf-8"))
        return digest.finalize().hex()

    def _key_conversion(self, public_key) -> str:
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return base64.b64encode(public_key_bytes).decode("utf-8")

    def get_sign(self, message: str, private_key) -> str:
        signature = private_key.sign(
            message.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return signature.hex()

    def proof_of_work(self, difficulty):
        new_proof = 1
        while True:
            hash_operation = self._get_hash(
                self.id + self.time + self.link + self.author + str(new_proof)
            )
            if hash_operation[:difficulty] == "0" * difficulty:
                return str(new_proof)
            new_proof += 1

    def calculate_difficulty(self):
        # Simple placeholder for difficulty calculation
        return 1

    def calculate_merkle_root(self, transactions):
        if not transactions:
            return ""

        def hash_pair(a, b):
            return self._get_hash(a + b)

        current_level = [
            self._get_hash(json.dumps(tx.get_dict())) for tx in transactions
        ]

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    next_level.append(hash_pair(current_level[i], current_level[i + 1]))
                else:
                    next_level.append(current_level[i])
            current_level = next_level

        return current_level[0]

    def add_transaction(self, transaction, sender_wallet, recipient_wallet):
        verified, message = transaction.verify_transaction(
            sender_wallet, recipient_wallet
        )
        if verified:
            self.transactions.append(transaction)
            self.tx_count = len(self.transactions)
            self.merkle_root = self.calculate_merkle_root(self.transactions)
            return True, "Transaction added successfully."
        return False, message

    def save_to_disk(self):
        block_data = self.get_dict()
        with open(f"block_{self.id}.json", "w") as f:
            json.dump(block_data, f)

    def get_dict(self):
        return self.__dict__


if __name__ == "__main__":
    private_key_path = "private_key.pem"
    public_key_path = "public_key.pem"

    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend()
        )

    # Example wallets
    sender_wallet = Wallet.load_from_disk("Alice") or Wallet("Alice", 100, public_key)
    recipient_wallet = Wallet.load_from_disk("Bob") or Wallet("Bob", 50, public_key)

    sender_wallet.save_to_disk()
    recipient_wallet.save_to_disk()

    prev_data = Block("previous data", None, [], private_key_path, public_key_path)
    b = Block("abc", prev_data, [], private_key_path, public_key_path)

    # Create a transaction
    tx = Transaction("Alice", "Bob", 10)
    tx.sign_transaction(private_key)

    # Verify and add the transaction
    success, message = b.add_transaction(tx, sender_wallet, recipient_wallet)
    print(message)

    b.save_to_disk()
    print(b.get_dict())
