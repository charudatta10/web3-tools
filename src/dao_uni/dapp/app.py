from flask import Flask, request, jsonify

from blockchain import Blockchain
from univ_dao import UniversityDAO
from smart_contract_handler import CustomSmartContractHandler

import sys

# setting path
sys.path.append('src/dao_uni')

from wallet import Wallet

app = Flask(__name__)

# Initialize blockchain and smart contract handler
genesis_wallet = Wallet()
blockchain = Blockchain(genesis_wallet)
university_dao = UniversityDAO()
contract_methods = [
    {"name": "CREATE_COURSE", "args": ["Intro to Blockchain", "Dr. Smith"]},
    {"name": "ENROLL_STUDENT", "args": [1, "Alice"]},
    {"name": "ISSUE_CERTIFICATE", "args": [1, "Alice"]},
    {"name": "VERIFY_CERTIFICATE", "args": [1, "Alice"]}
]
handler = CustomSmartContractHandler(blockchain, university_dao, contract_methods)

@app.route('/create_course', methods=['POST'])
def create_course():
    data = request.json
    result = university_dao.create_course(data['courseName'], data['instructor'])
    handler.deploy_contract(genesis_wallet)  # Deploy contract
    return jsonify({'message': result})

@app.route('/enroll_student', methods=['POST'])
def enroll_student():
    data = request.json
    result = university_dao.enroll_student(int(data['courseId']), data['studentName'])
    handler.execute_contract()  # Execute contract
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True)
