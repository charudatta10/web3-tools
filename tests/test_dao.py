import unittest
import os
from src.block import Block
from src.blockchain import Blockchain
from src.dao import DAO

class TestDAO(unittest.TestCase):

    def setUp(self):
        SECRET_KEY = os.getenv('BLOCK_SECRET_KEY')
        with open("Genesis-Token.txt", 'r') as file:
            genesis_token = file.read()
        self.dao = DAO(genesis_token, SECRET_KEY)

    def test_genesis_block(self):
        # Test if the genesis block is created correctly
        self.assertEqual(len(self.dao.chain), 1)
        self.assertEqual(self.dao.chain[0].payload["index"], 0)
        self.assertEqual(self.dao.chain[0].payload["transactions"], "Genesis Block")

    def test_add_member(self):
        # Test adding a member
        self.dao.add_member("1", {"name": "Alice"})
        self.assertIn("1", self.dao.members)
        self.assertEqual(self.dao.members["1"]["name"], "Alice")

    def test_create_proposal(self):
        # Test creating a proposal
        self.dao.create_proposal({"title": "New Project Funding", "amount": 1000})
        self.assertEqual(len(self.dao.proposals), 1)
        self.assertEqual(self.dao.proposals[0]["data"]["title"], "New Project Funding")

    def test_vote_proposal(self):
        # Test voting on a proposal
        self.dao.add_member("1", {"name": "Alice"})
        self.dao.create_proposal({"title": "New Project Funding", "amount": 1000})
        self.dao.vote_proposal("1", 0, "yes")
        self.assertEqual(self.dao.proposals[0]["votes"]["yes"], 1)

    def test_count_votes(self):
        # Test counting votes
        self.dao.add_member("1", {"name": "Alice"})
        self.dao.add_member("2", {"name": "Bob"})
        self.dao.create_proposal({"title": "New Project Funding", "amount": 1000})
        self.dao.vote_proposal("1", 0, "yes")
        self.dao.vote_proposal("2", 0, "no")
        self.dao.count_votes(0)
        self.assertIn("Proposal 0 failed with 1 yes votes and 1 no votes", self.dao.chain[-1].payload["transactions"]) or self.assertIn("failed", self.dao.chain[-1].payload["transactions"])

if __name__ == '__main__':
    unittest.main()
