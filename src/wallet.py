import os
import hashlib
import json
import jwt
import time
import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class Wallet:
    def __init__(self):
        self.private_key, self.public_key = self.generate_rsa_keys()
        self.address = self.compute_address()
        self.data = {}

    def generate_rsa_keys(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return private_pem, public_pem

    def compute_address(self):
        public_key_obj = serialization.load_pem_public_key(self.public_key)
        public_key_bytes = public_key_obj.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return hashlib.sha256(public_key_bytes).hexdigest()

    def get_private_key_obj(self):
        return serialization.load_pem_private_key(self.private_key, password=None)

    def get_public_key_obj(self):
        return serialization.load_pem_public_key(self.public_key)

    def save_wallet(self, filename):
        with open(filename, "w") as f:
            json.dump(
                {
                    "private_key": self.private_key.decode(),
                    "public_key": self.public_key.decode(),
                    "address": self.address,
                    "data": self.data,
                },
                f,
            )

    @staticmethod
    def load_wallet(filename):
        with open(filename, "r") as f:
            wallet_data = json.load(f)
            wallet = Wallet()
            wallet.private_key = wallet_data["private_key"].encode()
            wallet.public_key = wallet_data["public_key"].encode()
            wallet.address = wallet_data["address"]
            wallet.data = wallet_data["data"]
            return wallet
