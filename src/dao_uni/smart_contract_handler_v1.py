import json
from wallet import Wallet
from blockchain import Blockchain

class SmartContractHandler:
    def __init__(self, blockchain, contract_json):
        self.blockchain = blockchain
        self.contract_name = contract_json['contractName']
        self.abi = contract_json['abi']
        self.bytecode = contract_json['bytecode']
        self.deployed_contract = None

    def deploy_contract(self, initial_supply, owner_wallet):
        contract_data = {
            "contractName": self.contract_name,
            "abi": self.abi,
            "bytecode": self.bytecode,
            "initial_supply": initial_supply,
            "owner": owner_wallet.address
        }
        self.blockchain.add_block(f"Deploy Contract: {json.dumps(contract_data)}", owner_wallet)
        self.deployed_contract = contract_data
        print(f"Contract {self.contract_name} deployed with initial supply: {initial_supply}")

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

    contract_json = {
        "contractName": "University",
        "abi": [
            {"constant": True, "inputs": [], "name": "courseCount", "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
            {"constant": False, "inputs": [{"name": "name", "type": "string"}, {"name": "instructor", "type": "address"}], "name": "createCourse", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
            {"constant": False, "inputs": [{"name": "courseId", "type": "uint256"}], "name": "enrollStudent", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
            {"constant": False, "inputs": [{"name": "courseId", "type": "uint256"}, {"name": "student", "type": "address"}], "name": "issueCertificate", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
            {"constant": True, "inputs": [{"name": "courseId", "type": "uint256"}, {"name": "student", "type": "address"}], "name": "verifyCertificate", "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view", "type": "function"}
        ],
        "bytecode": "0x608060405234801561001057600080fd5b506040516104093803806104098339810160409081528151602080840191506000..."
    }

    smart_contract_handler = SmartContractHandler(blockchain, contract_json)

    # Deploy the contract
    initial_supply = 1000000
    smart_contract_handler.deploy_contract(initial_supply, genesis_wallet)

    # Interact with the contract (example: create course)
    instructor_wallet = Wallet()
    smart_contract_handler.call_contract_function('createCourse', 'Introduction to Blockchain', instructor_wallet.address)

    # Print the blockchain
    for block in blockchain.chain:
        print(block)
