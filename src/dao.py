import hashlib
import json
import time
import jwt
import os
from block import Block
from blockchain import Blockchain
from nft import NFT

class DAO(Blockchain):
    def __init__(self, genesis_token, key):
        super().__init__(genesis_token, key)
        self.members = {}
        self.proposals = []
        self.nfts = []

    def add_member(self, member_id, member_data):
        if member_id in self.members:
            print(f"Member {member_id} already exists.")
            return
        self.members[member_id] = member_data
        self.add_block(f"Member {member_id} added: {member_data}")
        print(f"Member {member_id} added.")

    def create_proposal(self, proposal_data):
        proposal_id = len(self.proposals)
        self.proposals.append({
            "id": proposal_id,
            "data": proposal_data,
            "votes": {"yes": 0, "no": 0}
        })
        self.add_block(f"Proposal {proposal_id} created: {proposal_data}")
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
        self.add_block(f"Member {member_id} voted {vote} on proposal {proposal_id}")
        print(f"Member {member_id} voted {vote} on proposal {proposal_id}")

    def count_votes(self, proposal_id):
        if proposal_id >= len(self.proposals):
            print("Invalid proposal ID")
            return
        votes = self.proposals[proposal_id]["votes"]
        result = "passed" if votes["yes"] > votes["no"] else "failed"
        self.add_block(f"Proposal {proposal_id} {result} with {votes['yes']} yes votes and {votes['no']} no votes")
        if result == "passed":
            self.execute_proposal(proposal_id)
        print(f"Proposal {proposal_id} has {result}")

    def execute_proposal(self, proposal_id):
        proposal = self.proposals[proposal_id]
        self.add_block(f"Proposal {proposal_id} executed: {proposal['data']}")
        print(f"Proposal {proposal_id} executed")

    def mint_nft(self, owner_id, metadata):
        nft_id = len(self.nfts)
        nft = NFT(nft_id, owner_id, metadata)
        self.nfts.append(nft)
        nft_data = nft.to_dict()
        self.add_block(f"NFT Minted: {nft_data}")
        print(f"NFT {nft_id} minted for owner {owner_id}")

    def get_nft_royalties(self, nft_id, sales_price, royalty_percentage):
        if nft_id >= len(self.nfts):
            print("Invalid NFT ID")
            return
        royalty_amount = sales_price * (royalty_percentage / 100)
        self.add_block(f"NFT {nft_id} generated royalties: {royalty_amount}")
        print(f"NFT {nft_id} generated royalties: {royalty_amount}")
        return royalty_amount

    def get_proposals(self):
        return self.proposals

# Example usage
SECRET_KEY = os.getenv('BLOCK_SECRET_KEY')
with open("Genesis-Token.txt", 'r') as file:
    genesis_token = file.read()

# Create the DAO
dao = DAO(genesis_token, SECRET_KEY)

# Add members to the DAO
dao.add_member("1", {"name": "Alice"})
dao.add_member("2", {"name": "Bob"})

# Mint NFTs
dao.mint_nft("1", {"name": "CryptoKitty", "attributes": {"color": "blue", "age": 2}})
dao.mint_nft("2", {"name": "CryptoPunk", "attributes": {"style": "punk", "generation": 1}})

# Calculate Royalties for NFT
dao.get_nft_royalties(0, 1000, 5)

# Create a proposal
dao.create_proposal({"title": "New Project Funding", "amount": 1000})

# Members vote on the proposal
dao.vote_proposal("1", 0, "yes")
dao.vote_proposal("2", 0, "no")

# Count votes and decide on the proposal
dao.count_votes(0)

# Check if the blockchain is valid
print("Is the blockchain valid?", dao.is_chain_valid())

# Print the blockchain
for block in dao.chain:
    print(block.payload)
