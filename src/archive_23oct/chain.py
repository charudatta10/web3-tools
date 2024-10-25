import json
import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


from src.wallet import Wallet
from src.transaction import Transaction
from src.block import Block


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.load_chain()

    def create_genesis_block(self, private_key_path, public_key_path):
        if not self.chain:
            genesis_block = Block(
                "Genesis Block", None, [], private_key_path, public_key_path
            )
            self.chain.append(genesis_block)
            self.save_chain()

    def add_block(self, block):
        self.chain.append(block)
        self.save_chain()

    def add_transaction(
        self, sender, recipient, amount, private_key_path, public_key_path
    ):
        sender_wallet = Wallet.load_from_disk(sender)
        recipient_wallet = Wallet.load_from_disk(recipient)

        if not sender_wallet or not recipient_wallet:
            return False, "Sender or recipient wallet does not exist."

        transaction = Transaction(sender, recipient, amount)
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None, backend=default_backend()
            )
        transaction.sign_transaction(private_key)

        last_block = self.chain[-1]
        success, message = last_block.add_transaction(
            transaction, sender_wallet, recipient_wallet
        )
        if success:
            self.current_transactions.append(transaction)
            self.save_chain()
        return success, message

    def mine_block(self, private_key_path, public_key_path):
        last_block = self.chain[-1]
        new_block = Block(
            "New Block",
            last_block,
            self.current_transactions,
            private_key_path,
            public_key_path,
        )
        self.current_transactions = []
        self.add_block(new_block)
        return new_block

    def save_chain(self):
        chain_data = [block.get_dict() for block in self.chain]
        with open("blockchain.json", "w") as f:
            json.dump(chain_data, f, indent=4)

    def load_chain(self):
        if os.path.exists("blockchain.json"):
            try:
                with open("blockchain.json", "r") as f:
                    chain_data = json.load(f)
                self.chain = [
                    self.dict_to_block(block_data) for block_data in chain_data
                ]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading blockchain: {e}")
                self.chain = []
        else:
            self.create_genesis_block("private_key.pem", "public_key.pem")

    def dict_to_block(self, block_data):
        block = Block(
            block_data["data"],
            None,
            [Transaction.from_dict(tx) for tx in block_data["transactions"]],
            "private_key.pem",
            "public_key.pem",
        )
        block.__dict__.update(block_data)
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.link != previous_block._get_hash(
                json.dumps(previous_block.get_dict(), sort_keys=True)
            ):
                return False

            if not current_block.proof_of_work(current_block.difficulty):
                return False

        return True
