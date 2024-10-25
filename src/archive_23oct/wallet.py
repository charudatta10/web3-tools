import json
import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class Wallet:
    def __init__(self, address, balance, public_key):
        self.address = address
        self.balance = balance
        self.public_key = public_key

    def save_to_disk(self):
        wallet_data = {
            "address": self.address,
            "balance": self.balance,
            "public_key": self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode("utf-8"),
        }
        with open(f"{self.address}.json", "w") as f:
            json.dump(wallet_data, f)

    @staticmethod
    def load_from_disk(address):
        if not os.path.exists(f"{address}.json"):
            return None
        with open(f"{address}.json", "r") as f:
            wallet_data = json.load(f)
        public_key = serialization.load_pem_public_key(
            wallet_data["public_key"].encode("utf-8"), backend=default_backend()
        )
        return Wallet(wallet_data["address"], wallet_data["balance"], public_key)
