import hashlib
import json
import time
import jwt
import logging
import libtorrent as lt
import os
import shutil
import base64
from cryptography.hazmat.primitives import serialization
from wallet import Wallet
from block import Block

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TorrentBlockchain:
    def __init__(self):
        self.session = lt.session()
        self.blocks_dir = 'blocks'
        self.wallet = Wallet()

        # Ensure the blocks directory exists
        if not os.path.exists(self.blocks_dir):
            os.makedirs(self.blocks_dir)

    def share_block(self, block, filename):
        block_file = os.path.join(self.blocks_dir, filename)
        with open(block_file, 'w') as f:
            f.write(block)

        # Create a torrent file for the block
        fs = lt.file_storage()
        lt.add_files(fs, block_file)
        t = lt.create_torrent(fs)
        t.set_creator('TorrentBlockchain')
        t.set_comment('A blockchain block')
        lt.set_piece_hashes(t, self.blocks_dir)
        torrent = t.generate()

        torrent_file = block_file + '.torrent'
        with open(torrent_file, 'wb') as f:
            f.write(lt.bencode(torrent))

        logging.info(f"Block shared: {block_file}")
        return torrent_file

    def download_block(self, torrent_file):
        info = lt.torrent_info(torrent_file)
        h = self.session.add_torrent({
            'ti': info,
            'save_path': self.blocks_dir
        })

        logging.info(f"Downloading block: {torrent_file}")
        while not h.is_seed():
            s = h.status()
            logging.info(f"Progress: {s.progress * 100}%")
            time.sleep(1)

        logging.info("Download complete")

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
