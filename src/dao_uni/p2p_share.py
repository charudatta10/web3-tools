import libtorrent as lt
import time
import json
from blockchain import Blockchain
from wallet import Wallet

class P2PBlockchain(Blockchain):
    def __init__(self, genesis_wallet):
        super().__init__(genesis_wallet)
        self.session = lt.session()
        self.torrents = []

    def add_torrent(self, torrent_path):
        info = lt.torrent_info(torrent_path)
        h = self.session.add_torrent({'ti': info, 'save_path': './'})
        self.torrents.append(h)
        print(f"Added torrent: {torrent_path}")
        
    def share_blockchain(self):
        blockchain_data = json.dumps([Block.verify_jwt(token, self.genesis_wallet.get_public_key_obj()) for token in self.chain])
        with open('blockchain_data.json', 'w') as f:
            f.write(blockchain_data)
        
        # Create a torrent file
        fs = lt.file_storage()
        lt.add_files(fs, './blockchain_data.json')
        t = lt.create_torrent(fs)
        t.set_comment("Blockchain data")
        t.set_creator("P2PBlockchain")
        lt.set_piece_hashes(t, '.')
        torrent = t.generate()

        torrent_path = 'blockchain_data.torrent'
        with open(torrent_path, 'wb') as f:
            f.write(lt.bencode(torrent))
        
        self.add_torrent(torrent_path)
        print(f"Blockchain data shared as torrent: {torrent_path}")
    
    def download_blockchain(self, torrent_path):
        self.add_torrent(torrent_path)
        h = self.torrents[-1]
        
        while not h.is_seed():
            s = h.status()
            print(f'Downloading: {s.progress * 100:.2f}% complete')
            time.sleep(1)
        
        with open('blockchain_data.json', 'r') as f:
            blockchain_data = json.load(f)
        
        self.chain = [Block.create_jwt(block, self.genesis_wallet.get_private_key_obj()) for block in blockchain_data]
        print("Blockchain data downloaded and integrated.")
    
    def __str__(self):
        return json.dumps([Block.verify_jwt(token, self.genesis_wallet.get_public_key_obj()).__str__() for token in self.chain], indent=4)


# Example usage
if __name__ == "__main__":
    genesis_wallet = Wallet()
    p2p_blockchain = P2PBlockchain(genesis_wallet)
    
    # Adding blocks to the blockchain
    p2p_blockchain.add_block("A-> B: 5", genesis_wallet)
    p2p_blockchain.add_block("B-> A: 2", genesis_wallet)
    
    # Share blockchain data as a torrent
    p2p_blockchain.share_blockchain()
    
    # Download blockchain data from a torrent
    p2p_blockchain.download_blockchain('blockchain_data.torrent')

    print("Is the blockchain valid?", p2p_blockchain.is_chain_valid())
    print(str(p2p_blockchain))
