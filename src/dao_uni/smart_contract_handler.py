import hashlib
import json
import time
from blockchain import Blockchain
from wallet import Wallet
from block import Block

class SmartContractHandler:
    def __init__(self, blockchain, contract_abi, contract_bytecode):
        self.blockchain = blockchain
        self.contract_abi = contract_abi
        self.contract_bytecode = contract_bytecode
        self.deployed_contract = None

    def deploy_contract(self, initial_supply, owner_wallet):
        contract_data = {
            "abi": self.contract_abi,
            "bytecode": self.contract_bytecode,
            "initial_supply": initial_supply,
            "owner": owner_wallet.address
        }
        self.blockchain.add_block(f"Deploy Contract: {json.dumps(contract_data)}", owner_wallet)
        self.deployed_contract = contract_data
        print(f"Contract deployed with initial supply: {initial_supply}")

    def call_contract_function(self, function_name, *args):
        if not self.deployed_contract:
            print("No deployed contract found")
            return

        function_call = {
            "function": function_name,
            "args": args
        }
        self.blockchain.add_block(f"Call Contract Function: {json.dumps(function_call)}", self.blockchain.genesis_wallet)
        print(f"Called function {function_name} with args {args}")

# Example Usage
if __name__ == "__main__":
    genesis_wallet = Wallet()
    blockchain = Blockchain(genesis_wallet)

    # Example ABI and Bytecode (these should be actual values from Solidity compiler)
    contract_abi = [
        {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [{"name": "", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": False, "inputs": [{"name": "to", "type": "address"}, {"name": "value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"inputs": [{"name": "initialSupply", "type": "uint256"}], "payable": False, "stateMutability": "nonpayable", "type": "constructor"}
    ]
    contract_bytecode = "0x608060405234801561001057600080fd5b506040516104093803806104098339810160409081528151602080840191506000..."

    smart_contract_handler = SmartContractHandler(blockchain, contract_abi, contract_bytecode)

    # Deploy the contract
    initial_supply = 1000000
    smart_contract_handler.deploy_contract(initial_supply, genesis_wallet)

    # Interact with the contract (example: transfer tokens)
    recipient_address = "0xRecipientAddress"
    amount_to_transfer = 1000
    smart_contract_handler.call_contract_function("transfer", recipient_address, amount_to_transfer)

    # Print the blockchain
    for block in blockchain.chain:
        print(block)
