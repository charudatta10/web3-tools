import hashlib
import json
import time
import jwt
import os
from block import Block
from blockchain import Blockchain
from wallet import Wallet

class DAO(Blockchain):
    def __init__(self, genesis_wallet):
        super().__init__(genesis_wallet)
        self.members = {}
        self.proposals = []

    def add_member(self, member_id, member_data):
        if member_id in self.members:
            print(f"Member {member_id} already exists.")
            return
        self.members[member_id] = member_data
        transaction = f"Member {member_id} added: {member_data}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Member {member_id} added.")

    def create_proposal(self, proposal_data):
        proposal_id = len(self.proposals)
        self.proposals.append(
            {"id": proposal_id, "data": proposal_data, "votes": {"yes": 0, "no": 0}}
        )
        transaction = f"Proposal {proposal_id} created: {proposal_data}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Proposal {proposal_id} created.")

    def vote_proposal(self, member_id, proposal_id, vote):
        if proposal_id >= len(self.proposals):
            print("Invalid proposal ID")
            return
        if vote not in ["yes", "no"]:
            print("Invalid vote")
            return
        if member_id not in self.members:
            print(f"Member {member_id} does not exist")
            return
        self.proposals[proposal_id]["votes"][vote] += 1
        transaction = f"Member {member_id} voted {vote} on proposal {proposal_id}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Member {member_id} voted {vote} on proposal {proposal_id}")

    def count_votes(self, proposal_id):
        if proposal_id >= len(self.proposals):
            print("Invalid proposal ID")
            return
        votes = self.proposals[proposal_id]["votes"]
        result = "passed" if votes["yes"] > votes["no"] else "failed"
        transaction = f"Proposal {proposal_id} {result} with {votes['yes']} yes votes and {votes['no']} no votes"
        self.add_block(transaction, self.genesis_wallet)
        if result == "passed":
            self.execute_proposal(proposal_id)
        print(f"Proposal {proposal_id} has {result}")

    def execute_proposal(self, proposal_id):
        proposal = self.proposals[proposal_id]
        transaction = f"Proposal {proposal_id} executed: {proposal['data']}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Proposal {proposal_id} executed")

    def get_proposals(self):
        return self.proposals


# Example usage
genesis_wallet = Wallet()
blockchain = DAO(genesis_wallet)

# Add members to the DAO
blockchain.add_member("1", {"name": "Alice"})
blockchain.add_member("2", {"name": "Bob"})

# Create a proposal
blockchain.create_proposal({"title": "New Project Funding", "amount": 1000})

# Members vote on the proposal
blockchain.vote_proposal("1", 0, "yes")
blockchain.vote_proposal("2", 0, "no")

# Count votes and decide on the proposal
blockchain.count_votes(0)

# Check if the blockchain is valid
print("Is the blockchain valid?", blockchain.is_chain_valid())

# Print the blockchain
for block in blockchain.chain:
    print(block)
