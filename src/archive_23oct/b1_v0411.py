import hashlib
import json
import time
import jwt
import os
from block import Block
from blockchain import Blockchain
from nft import NFT


class Torrent:
    def __init__(self, torrent_id, data):
        self.torrent_id = torrent_id
        self.data = data
        self.peers = []
        self.dht = {}  # For simplicity, using a dictionary to simulate DHT

    def generate_torrent_file(self):
        torrent_file = {
            "torrent_id": self.torrent_id,
            "data_hash": self.compute_hash(self.data),
            "created_at": time.time(),
            "peers": self.peers,
        }
        with open(f"torrent_{self.torrent_id}.json", "w") as f:
            json.dump(torrent_file, f, indent=4)
        print(f"Torrent file generated: torrent_{self.torrent_id}.json")

    def compute_hash(self, data):
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()

    def add_peer(self, peer_id, peer_info):
        self.peers.append({"peer_id": peer_id, "info": peer_info})
        self.dht[peer_id] = peer_info
        print(f"Peer {peer_id} added: {peer_info}")

    def get_peers(self):
        return self.peers


### Server and Peer Classes:

# python
import socket
import threading


class P2PServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started at {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode("utf-8")
                if data:
                    print(f"Received: {data}")
                    self.broadcast(data, client_socket)
                else:
                    break
            except:
                break
        client_socket.close()

    def broadcast(self, data, client_socket):
        for peer in self.peers:
            if peer != client_socket:
                try:
                    peer.send(data.encode("utf-8"))
                except:
                    peer.close()
                    self.peers.remove(peer)


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect_to_server(self, server_host, server_port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))

        while True:
            data = input("Enter message: ")
            client_socket.send(data.encode("utf-8"))

            server_response = client_socket.recv(1024).decode("utf-8")
            print(f"Received from server: {server_response}")


### Integration with DAO:


# python
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
        self.proposals.append(
            {"id": proposal_id, "data": proposal_data, "votes": {"yes": 0, "no": 0}}
        )
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
        self.add_block(
            f"Proposal {proposal_id} {result} with {votes['yes']} yes votes and {votes['no']} no votes"
        )
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


### Example usage with Torrent Class

# python
SECRET_KEY = os.getenv("BLOCK_SECRET_KEY")
with open("Genesis-Token.txt", "r") as file:
    genesis_token = file.read()

# Create the DAO
dao = DAO(genesis_token, SECRET_KEY)

# Add members to the DAO
dao.add_member("1", {"name": "Alice"})
dao.add_member("2", {"name": "Bob"})

# Mint NFTs
dao.mint_nft("1", {"name": "CryptoKitty", "attributes": {"color": "blue", "age": 2}})
dao.mint_nft(
    "2", {"name": "CryptoPunk", "attributes": {"style": "punk", "generation": 1}}
)

# Create a Torrent for NFT sharing
nft_torrent = Torrent(0, dao.nfts[0].to_dict())
nft_torrent.generate_torrent_file()

# Add Peers
nft_torrent.add_peer("peer1", {"host": "127.0.0.1", "port": 8000})
nft_torrent.add_peer("peer2", {"host": "127.0.0.1", "port": 8001})

# Start P2P Server
server = P2PServer("127.0.0.1", 8000)
threading.Thread(target=server.start_server).start()

# Connect Peers
peer1 = Peer("127.0.0.1", 8000)
threading.Thread(target=peer1.connect_to_server, args=("127.0.0.1", 8000)).start()

peer2 = Peer("127.0.0.1", 8001)
threading.Thread(target=peer2.connect_to_server, args=("127.0.0.1", 8000)).start()

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
