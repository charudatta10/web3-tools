import hashlib
import json
import time
import jwt
import logging
from block import Block
from blockchain import Blockchain
from wallet import Wallet
from dao import DAO  # Assuming DAO is in a separate file called dao.py

class UniversityDAO(DAO):
    def __init__(self, genesis_wallet):
        super().__init__(genesis_wallet)
        self.courses = {}
        self.certificates = {}

    # Course Management
    def create_course(self, course_id, course_data):
        if course_id in self.courses:
            print(f"Course {course_id} already exists.")
            return
        self.courses[course_id] = course_data
        transaction = f"Course {course_id} created: {course_data}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Course {course_id} created.")

    def enroll_student(self, course_id, student_id):
        if course_id not in self.courses:
            print(f"Course {course_id} does not exist.")
            return
        if "students" not in self.courses[course_id]:
            self.courses[course_id]["students"] = []
        self.courses[course_id]["students"].append(student_id)
        transaction = f"Student {student_id} enrolled in course {course_id}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Student {student_id} enrolled in course {course_id}")

    # Certification
    def issue_certificate(self, course_id, student_id, certificate_data):
        certificate_id = f"{course_id}-{student_id}"
        if certificate_id in self.certificates:
            print(f"Certificate {certificate_id} already issued.")
            return
        self.certificates[certificate_id] = certificate_data
        transaction = f"Certificate {certificate_id} issued: {certificate_data}"
        self.add_block(transaction, self.genesis_wallet)
        print(f"Certificate {certificate_id} issued.")

    def verify_certificate(self, certificate_id):
        if certificate_id in self.certificates:
            print(f"Certificate {certificate_id} is valid.")
            return True
        print(f"Certificate {certificate_id} is not valid.")
        return False

# Example usage
if __name__ == "__main__":
    genesis_wallet = Wallet()
    university_dao = UniversityDAO(genesis_wallet)

    # Add members to the DAO
    university_dao.add_member("1", {"name": "Alice"})
    university_dao.add_member("2", {"name": "Bob"})

    # Create a course
    university_dao.create_course("CS101", {"title": "Introduction to Computer Science", "instructor": "Dr. Smith"})

    # Enroll students in the course
    university_dao.enroll_student("CS101", "1")
    university_dao.enroll_student("CS101", "2")

    # Issue certificates to students
    university_dao.issue_certificate("CS101", "1", {"grade": "A"})
    university_dao.issue_certificate("CS101", "2", {"grade": "B"})

    # Verify certificates
    university_dao.verify_certificate("CS101-1")
    university_dao.verify_certificate("CS101-2")

    # Check if the blockchain is valid
    print("Is the blockchain valid?", university_dao.is_chain_valid())

    # Print the blockchain
    for block in university_dao.chain:
        print(block)
