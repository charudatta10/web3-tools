import unittest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from src.chain import Blockchain

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

        # Initialize blockchain
        self.blockchain = Blockchain()

    def test_create_genesis_block(self):
        self.blockchain.create_genesis_block(self.private_key_path, self.public_key_path)
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].data, "Genesis Block")

    def test_add_transaction(self):
        self.blockchain.create_genesis_block(self.private_key_path, self.public_key_path)
        success, message = self.blockchain.add_transaction("Alice", "Bob", 10, self.private_key_path, self.public_key_path)
        self.assertTrue(success, message)
        self.assertEqual(len(self.blockchain.current_transactions), 1)

    def test_mine_block(self):
        self.blockchain.create_genesis_block(self.private_key_path, self.public_key_path)
        self.blockchain.add_transaction("Alice", "Bob", 10, self.private_key_path, self.public_key_path)
        new_block = self.blockchain.mine_block(self.private_key_path, self.public_key_path)
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(new_block.tx_count, 1)

    def test_chain_validity(self):
        self.blockchain.create_genesis_block(self.private_key_path, self.public_key_path)
        self.blockchain.add_transaction("Alice", "Bob", 10, self.private_key_path, self.public_key_path)
        self.blockchain.mine_block(self.private_key_path, self.public_key_path)
        self.assertTrue(self.blockchain.is_chain_valid())

    def test_block_persistence(self):
        self.blockchain.create_genesis_block(self.private_key_path, self.public_key_path)
        self.blockchain.save_chain()
        self.blockchain.load_chain()
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].data, "Genesis Block")

if __name__ == "__main__":
    unittest.main()