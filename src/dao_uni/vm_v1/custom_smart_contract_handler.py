from uni_dao import UniversityDAO
from custom_compiler import CustomCompiler
from custom_vm import CustomVM

import os
import sys
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
    def __init__(self, blockchain, university_dao, contract_methods):
        self.blockchain = blockchain
        self.compiler = CustomCompiler()
        self.university_dao = university_dao
        self.contract_methods = contract_methods

    def deploy_contract(self, wallet):
        bytecode = self.compiler.compile(self.contract_methods)
        self.blockchain.add_block(f"Deploy Contract: {bytecode}", wallet)
        print(f"Contract deployed with bytecode: {bytecode}")

    def execute_contract(self):
        bytecode = self.compiler.compile(self.contract_methods)
        vm = CustomVM(self.university_dao)
        vm.memory = [
            "Intro to Blockchain".encode('utf-8').hex(), 
            "Dr. Smith".encode('utf-8').hex(), 
            "1".encode('utf-8').hex(), 
            "Alice".encode('utf-8').hex(), 
            "1".encode('utf-8').hex(), 
            "Alice".encode('utf-8').hex(), 
            "1".encode('utf-8').hex(), 
            "Alice".encode('utf-8').hex()
        ]
        vm.execute(bytecode)
        print(f"Contract executed. Memory: {vm.memory}")

# Example usage
if __name__ == "__main__":
    genesis_wallet = Wallet()
    blockchain = Blockchain(genesis_wallet)

    contract_methods = [
        {"name": "create_course", "args": ["Intro to Blockchain", "Dr. Smith"]},
        {"name": "enroll_student", "args": [1, "Alice"]},
        {"name": "issue_certificate", "args": [1, "Alice"]},
        {"name": "verify_certificate", "args": [1, "Alice"]}
    ]

    university_dao = UniversityDAO()
    handler = CustomSmartContractHandler(blockchain, university_dao, contract_methods)
    handler.deploy_contract(genesis_wallet)
    handler.execute_contract()

    # Print the blockchain
    for block in blockchain.chain:
        print(block)