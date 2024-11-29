import hashlib
import json
import time
import jwt
import logging
import os
import qbittorrentapi
from cryptography.hazmat.primitives import serialization
from wallet import Wallet
from block import Block

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TorrentBlockchain:
    def __init__(self):
        self.client = qbittorrentapi.Client(host='http://127.0.0.1:8080')
        try:
            self.client.auth_log_in(username='admin', password='adminadmin')  # Default credentials, make sure to update it for security
        except qbittorrentapi.LoginFailed as e:
            logging.error(f"Failed to login to qBittorrent: {e}")
        self.blocks_dir = 'blocks'
        self.wallet = Wallet()

        # Ensure the blocks directory exists
        if not os.path.exists(self.blocks_dir):
            os.makedirs(self.blocks_dir)

    def share_block(self, block, filename):
        block_file = os.path.join(self.blocks_dir, filename)
        with open(block_file, 'w') as f:
            f.write(block)

        # Create a torrent file for the block using qBittorrent Web UI
        torrent_file = block_file + '.torrent'
        try:
            self.client.torrents_create(category="blockchain", save_path=self.blocks_dir, urls=[block_file])
            logging.info(f"Block shared: {block_file}")
        except Exception as e:
            logging.error(f"Failed to create torrent: {e}")
        
        return torrent_file

    def download_block(self, torrent_file):
        try:
            with open(torrent_file, 'rb') as f:
                torrent_data = f.read()
            self.client.torrents_add(torrent_files=torrent_data, save_path=self.blocks_dir)
            logging.info(f"Downloading block: {torrent_file}")

            # Wait for the download to complete
            while not any(torrent.state_enum.is_complete for torrent in self.client.torrents_info()):
                time.sleep(1)
                logging.info("Waiting for the download to complete...")

            logging.info("Download complete")
        except Exception as e:
            logging.error(f"Failed to download block: {e}")

    def validate_chain(self):
        block_files = [f for f in os.listdir(self.blocks_dir) if f.endswith('.json')]
        block_files.sort()  # Ensure blocks are in order by filename

        previous_hash = "0"
        for block_file in block_files:
            with open(os.path.join(self.blocks_dir, block_file), 'r') as f:
                block_data = json.load(f)
                block_hash = block_data['hash']
                del block_data['hash']
                computed_hash = Block.compute_hash(block_data)

                if block_hash != computed_hash or block_data['previous_hash'] != previous_hash:
                    logging.error(f"Block {block_file} is invalid")
                    return False

                previous_hash = block_hash

        logging.info("All blocks are valid")
        return True

# Example usage
if __name__ == '__main__':
    blockchain = TorrentBlockchain()

    # Create and share a genesis block
    genesis_token = Block.create_genesis_token(blockchain.wallet.private_key)
    torrent_file = blockchain.share_block(genesis_token, 'genesis_block.json')

    # Simulate downloading the block
    blockchain.download_block(torrent_file)

    # Validate the chain
    blockchain.validate_chain()
