import time

class Blockchain:
    def __init__(self, genesis_wallet):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)
        self.genesis_wallet = genesis_wallet

    def create_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_block(self, transaction, wallet):
        self.current_transactions.append({
            'sender': wallet.address,
            'transaction': transaction
        })
        self.create_block(proof=123)

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
