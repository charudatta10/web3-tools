import hashlib
import json
import time


class NFT:
    def __init__(self, nft_id, owner_id, metadata):
        self.nft_id = nft_id
        self.owner_id = owner_id
        self.metadata = metadata
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "nft_id": self.nft_id,
            "owner_id": self.owner_id,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def compute_hash(nft_data):
        nft_string = json.dumps(nft_data, sort_keys=True)
        return hashlib.sha256(nft_string.encode()).hexdigest()
