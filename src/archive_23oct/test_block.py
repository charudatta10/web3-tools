import unittest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import json 

from src.wallet import Wallet
from src.transaction import Transaction
from src.block import Block

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        # Load keys
        self.private_key_path = "private_key.pem"
        self.public_key_path = "public_key.pem"

        with open(self.private_key_path, "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        with open(self.public_key_path, "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        # Create wallets
        self.sender_wallet = Wallet.load_from_disk("Alice") or Wallet("Alice", 100, self.public_key)
        self.recipient_wallet = Wallet.load_from_disk("Bob") or Wallet("Bob", 50, self.public_key)

        self.sender_wallet.save_to_disk()
        self.recipient_wallet.save_to_disk()

        # Create genesis block
        self.genesis_block = Block("Genesis Block", None, [], self.private_key_path, self.public_key_path)

    def test_create_transaction(self):
        # Create a transaction
        tx = Transaction("Alice", "Bob", 10)
        tx.sign_transaction(self.private_key)

        # Verify and add the transaction
        success, message = self.genesis_block.add_transaction(tx, self.sender_wallet, self.recipient_wallet)
        self.assertTrue(success, message)

    def test_insufficient_balance(self):
        # Create a transaction with insufficient balance
        tx = Transaction("Alice", "Bob", 200)
        tx.sign_transaction(self.private_key)

        # Verify and add the transaction
        success, message = self.genesis_block.add_transaction(tx, self.sender_wallet, self.recipient_wallet)
        self.assertFalse(success, message)

    def test_invalid_signature(self):
        # Create a transaction
        tx = Transaction("Alice", "Bob", 10)
        tx.signature = "00" * 64  # Invalid but correctly formatted signature

        # Verify and add the transaction
        success, message = self.genesis_block.add_transaction(tx, self.sender_wallet, self.recipient_wallet)
        self.assertFalse(success, message)

    def test_block_persistence(self):
        # Save block to disk
        self.genesis_block.save_to_disk()

        # Load block from disk
        with open(f'block_{self.genesis_block.id}.json', 'r') as f:
            block_data = json.load(f)

        self.assertEqual(block_data['id'], self.genesis_block.id)
        self.assertEqual(block_data['data'], self.genesis_block.data)

if __name__ == "__main__":
    unittest.main()
