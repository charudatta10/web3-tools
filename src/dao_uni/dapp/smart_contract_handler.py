import sys
sys.path.append('src/dao_uni')
from vm.custom_compiler import CustomCompiler

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
            "13", "49", "6e", "74", "72", "6f", "20", "74", "6f", "20", "42", "6c", "6f", "63", "6b", "63", "68", "61", "69", "6e", 
            "09", "44", "72", "2e", "20", "53", "6d", "69", "74", "68", 
            "01", 
            "05", "41", "6c", "69", "63", "65",
            "01",  # Course ID for ISSUE_CERTIFICATE and VERIFY_CERTIFICATE
            "05", "41", "6c", "69", "63", "65"  # Student name for ISSUE_CERTIFICATE and VERIFY_CERTIFICATE
        ]
        vm.execute(bytecode)
