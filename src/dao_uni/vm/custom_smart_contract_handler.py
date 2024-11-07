

import sys

from custom_compiler import CustomCompiler
from custom_vm import CustomVM


import os

# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
print(current_directory)
# setting path
sys.path.append('src/dao_uni')

# importing
from blockchain import Blockchain
from wallet import Wallet

class CustomSmartContractHandler:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.compiler = CustomCompiler()

    def deploy_contract(self, abi, wallet):
        bytecode = self.compiler.compile(abi)
        self.blockchain.add_block(f"Deploy Contract: {bytecode}", wallet)
        print(f"Contract deployed with bytecode: {bytecode}")

    def execute_contract(self, bytecode):
        vm = CustomVM()
        vm.execute(bytecode)
        print(f"Contract executed. Memory: {vm.memory}, Stack: {vm.stack}")

# Example usage
if __name__ == "__main__":
    genesis_wallet = Wallet()
    blockchain = Blockchain(genesis_wallet)

    contract_abi = [
        {"name": "LOAD", "inputs": [{"type": "uint256"}]},
        {"name": "ADD", "inputs": []},
        {"name": "STORE", "inputs": [{"type": "uint256"}]}
    ]

    handler = CustomSmartContractHandler(blockchain)
    handler.deploy_contract(contract_abi, genesis_wallet)
    
    # Get the bytecode from the blockchain (simplified here)
    bytecode = "01050103050209"  # This would be stored in the blockchain
    handler.execute_contract(bytecode)

    # Print the blockchain
    for block in blockchain.chain:
        print(block)
