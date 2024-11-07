from blockchain import Blockchain
from wallet import Wallet
from smart_contract_handler import SmartContractHandler

class UniversityDAO(Blockchain):
    def __init__(self, genesis_wallet, contract_abi, contract_bytecode):
        super().__init__(genesis_wallet)
        self.smart_contract_handler = SmartContractHandler(self, contract_abi, contract_bytecode)
        self.smart_contract_handler.deploy_contract(0, genesis_wallet)  # Deploy contract without initial supply

    # Course Management
    def create_course(self, course_name, instructor_wallet):
        self.smart_contract_handler.call_contract_function('createCourse', course_name, instructor_wallet.address)
        print(f"Course '{course_name}' created with instructor {instructor_wallet.address}")

    def enroll_student(self, course_id, student_wallet):
        self.smart_contract_handler.call_contract_function('enrollStudent', course_id)
        print(f"Student {student_wallet.address} enrolled in course {course_id}")

    # Certification
    def issue_certificate(self, course_id, student_wallet):
        self.smart_contract_handler.call_contract_function('issueCertificate', course_id, student_wallet.address)
        print(f"Certificate issued for student {student_wallet.address} in course {course_id}")

    def verify_certificate(self, course_id, student_wallet):
        result = self.smart_contract_handler.call_contract_function('verifyCertificate', course_id, student_wallet.address)
        if result:
            print(f"Certificate for student {student_wallet.address} in course {course_id} is valid")
        else:
            print(f"Certificate for student {student_wallet.address} in course {course_id} is not valid")

# Example usage
if __name__ == "__main__":
    genesis_wallet = Wallet()
    contract_abi = [
        {"constant": True, "inputs": [], "name": "courseCount", "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": False, "inputs": [{"name": "name", "type": "string"}, {"name": "instructor", "type": "address"}], "name": "createCourse", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": False, "inputs": [{"name": "courseId", "type": "uint256"}], "name": "enrollStudent", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": False, "inputs": [{"name": "courseId", "type": "uint256"}, {"name": "student", "type": "address"}], "name": "issueCertificate", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": True, "inputs": [{"name": "courseId", "type": "uint256"}, {"name": "student", "type": "address"}], "name": "verifyCertificate", "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view", "type": "function"}
    ]
    contract_bytecode = "0x608060405234801561001057600080fd5b506040516104093803806104098339810160409081528151602080840191506000..."

    university_dao = UniversityDAO(genesis_wallet, contract_abi, contract_bytecode)

    # Create a course
    instructor_wallet = Wallet()
    university_dao.create_course("Introduction to Blockchain", instructor_wallet)

    # Enroll a student in the course
    student_wallet = Wallet()
    university_dao.enroll_student(1, student_wallet)

    # Issue a certificate to the student
    university_dao.issue_certificate(1, student_wallet)

    # Verify the certificate
    university_dao.verify_certificate(1, student_wallet)

    # Print the blockchain
    for block in university_dao.chain:
        print(block)
