from blockchain import Blockchain
from wallet import Wallet
from smart_contract_handler import SmartContractHandler

class DAOWithSmartContracts(Blockchain):
    def __init__(self, genesis_wallet, contract_abi, contract_bytecode):
        super().__init__(genesis_wallet)
        self.members = {}
        self.proposals = []
        self.smart_contract_handler = SmartContractHandler(self, contract_abi, contract_bytecode)

    def add_member(self, member_id, member_data):
        if member_id in self.members:
            print(f"Member {member_id} already exists.")
            return
        self.members[member_id] = member_data
        transaction = f"Member {member_id} added: {member_data}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Member {member_id} added.")

    def create_proposal(self, proposal_data):
        proposal_id = len(self.proposals)
        self.proposals.append(
            {"id": proposal_id, "data": proposal_data, "votes": {"yes": 0, "no": 0}}
        )
        transaction = f"Proposal {proposal_id} created: {proposal_data}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Proposal {proposal_id} created.")

    def vote_proposal(self, member_id, proposal_id, vote):
        if proposal_id >= len(self.proposals):
            print("Invalid proposal ID")
            return
        if vote not in ["yes", "no"]:
            print("Invalid vote")
            return
        if member_id not in self.members:
            print(f"Member {member_id} does not exist")
            return
        self.proposals[proposal_id]["votes"][vote] += 1
        transaction = f"Member {member_id} voted {vote} on proposal {proposal_id}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Member {member_id} voted {vote} on proposal {proposal_id}")

    def count_votes(self, proposal_id):
        if proposal_id >= len(self.proposals):
            print("Invalid proposal ID")
            return
        votes = self.proposals[proposal_id]["votes"]
        result = "passed" if votes["yes"] > votes["no"] else "failed"
        transaction = f"Proposal {proposal_id} {result} with {votes['yes']} yes votes and {votes['no']} no votes"
        self.add_block(transaction, self.genesis_wallet)
        if result == "passed":
            self.execute_proposal(proposal_id)
        print(f"Proposal {proposal_id} has {result}")

    def execute_proposal(self, proposal_id):
        proposal = self.proposals[proposal_id]
        transaction = f"Proposal {proposal_id} executed: {proposal['data']}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Proposal {proposal_id} executed")

    def deploy_smart_contract(self, initial_supply, owner_wallet):
        self.smart_contract_handler.deploy_contract(initial_supply, owner_wallet)

    def interact_with_smart_contract(self, function_name, *args):
        self.smart_contract_handler.call_contract_function(function_name, *args)

    def get_proposals(self):
        return self.proposals

# Example usage
if __name__ == "__main__":
    genesis_wallet = Wallet()
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

    dao = DAOWithSmartContracts(genesis_wallet, contract_abi, contract_bytecode)

    # Add members to the DAO
    dao.add_member("1", {"name": "Alice"})
    dao.add_member("2", {"name": "Bob"})

    # Create a proposal
    dao.create_proposal({"title": "New Project Funding", "amount": 1000})

    # Members vote on the proposal
    dao.vote_proposal("1", 0, "yes")
    dao.vote_proposal("2", 0, "no")

    # Count votes and decide on the proposal
    dao.count_votes(0)

    # Deploy the smart contract
    initial_supply = 1000000
    dao.deploy_smart_contract(initial_supply, genesis_wallet)

    # Interact with the smart contract (example: transfer tokens)
    recipient_address = "0xRecipientAddress"
    amount_to_transfer = 1000
    dao.interact_with_smart_contract("transfer", recipient_address, amount_to_transfer)

    # Check if the blockchain is valid
    print("Is the blockchain valid?", dao.is_chain_valid())

    # Print the blockchain
    for block in dao.chain:
        print(block)
