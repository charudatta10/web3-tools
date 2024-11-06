import hashlib
import json
import time
from blockchain import Blockchain
from wallet import Wallet
from block import Block
import logging

# Not Working

class NFT:
    def __init__(self, blockchain=None):
        self.blockchain = blockchain if blockchain else self.create_blockchain()

    def create_blockchain(self):
        genesis_wallet = Wallet()
        blockchain = Blockchain(genesis_wallet)
        self.genesis_wallet = genesis_wallet
        return blockchain

    def to_dict(self, nft_id, owner_id, metadata):
        return {
            "nft_id": nft_id,
            "owner_id": owner_id,
            "metadata": metadata,
            "timestamp": time.time(),
        }

    @staticmethod
    def compute_hash(nft_data):
        nft_string = json.dumps(nft_data, sort_keys=True)
        return hashlib.sha256(nft_string.encode()).hexdigest()

    def exists_on_blockchain(self, check_type, identifier):
        for block in self.blockchain.chain:
            b1 = Block.verify_jwt(block, self.blockchain.genesis_wallet.get_public_key_obj())
            for transaction in b1["transactions"]:
                logging.debug(f"Checking transaction: {transaction}")
                if check_type == "wallet":
                    if f"Wallet Creation: {identifier}" in transaction:
                        logging.debug(f"Found wallet {identifier} in transaction.")
                        return True
                elif check_type.startswith("nft_"):
                    if "NFT Minted" in transaction:
                        try:
                            nft_data = json.loads(transaction.split(": ", 1)[1])
                            logging.debug(f"Checking NFT data: {nft_data}")
                            if check_type == "nft_meta" and nft_data["metadata"] == identifier:
                                logging.debug(f"Found NFT with metadata {identifier}.")
                                return True
                            if check_type == "nft_id" and nft_data["nft_id"] == identifier:
                                logging.debug(f"Found NFT with ID {identifier}.")
                                return True
                        except json.JSONDecodeError as e:
                            logging.error(f"JSON decode error: {e}")
        return False

    def wallet_exists_on_blockchain(self, wallet_address):
        return self.exists_on_blockchain("wallet", wallet_address)

    def nft_exists_on_blockchain_meta(self, metadata):
        return self.exists_on_blockchain("nft_meta", metadata)

    def nft_exists_on_blockchain_id(self, nft_id):
        return self.exists_on_blockchain("nft_id", nft_id)

    def mint_nft(self, owner_wallet, metadata):
        if not self.wallet_exists_on_blockchain(owner_wallet.address):
            logging.info(f"Owner wallet {owner_wallet.address} does not exist on the blockchain.")
            return
        if self.nft_exists_on_blockchain_meta(metadata): 
            logging.info(f"An NFT with similar metadata already exists on the blockchain.") 
            return
        nft_id = len(self.blockchain.chain)
        nft_data = self.to_dict(nft_id, owner_wallet.address, metadata)
        self.blockchain.add_block(f"NFT Minted: {json.dumps(nft_data)}", self.blockchain.genesis_wallet)
        logging.info(f"NFT {nft_id} minted for owner {owner_wallet.address}")

    def get_nft_royalties(self, nft_id, sales_price, royalty_percentage):
        if not self.nft_exists_on_blockchain_id(nft_id):
            logging.error("Invalid NFT ID")
            return
        royalty_amount = sales_price * (royalty_percentage / 100)
        self.blockchain.add_block(f"NFT {nft_id} generated royalties: {royalty_amount}", self.blockchain.genesis_wallet)
        logging.info(f"NFT {nft_id} generated royalties: {royalty_amount}")
        return royalty_amount

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    genesis_wallet = Wallet()
    blockchain = Blockchain(genesis_wallet)
    
    # Create NFT instance with existing blockchain reference
    nft = NFT(blockchain)

    # Adding wallets to the blockchain
    wallet1 = Wallet()
    wallet2 = Wallet()
    blockchain.add_block(f"Wallet Creation: {wallet1.address}", genesis_wallet)
    blockchain.add_block(f"Wallet Creation: {wallet2.address}", genesis_wallet)

    # Mint NFTs
    nft.mint_nft(wallet1, {"name": "CryptoKitty", "attributes": {"color": "blue", "age": 2}})
    nft.mint_nft(wallet2, {"name": "CryptoPunk", "attributes": {"style": "punk", "generation": 1}})
    nft.mint_nft(wallet2, {"name": "CryptoPunk", "attributes": {"style": "punk", "generation": 1}})
    # Calculate Royalties for NFT
    nft.get_nft_royalties(4, 1000, 5)
    nft.get_nft_royalties(0, 1000, 5)
