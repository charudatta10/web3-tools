from uni_dao import UniversityDAO
from custom_compiler import CustomCompiler

class CustomVM:
    def __init__(self, university_dao):
        self.university_dao = university_dao
        self.memory = []
        self.instruction_pointer = 0

    def execute(self, bytecode):
        print("Starting bytecode execution...")
        while self.instruction_pointer < len(bytecode):
            opcode = bytecode[self.instruction_pointer:self.instruction_pointer + 2]
            self.instruction_pointer += 2
            print(f"Executing opcode: {opcode}")
            if opcode == "01":  # CREATE_COURSE
                course_name = self.decode_string()
                instructor = self.decode_string()
                print(f"Decoded course_name: {course_name}, instructor: {instructor}")
                print(self.university_dao.create_course(course_name, instructor))
            elif opcode == "02":  # ENROLL_STUDENT
                course_id = self.decode_int()
                student = self.decode_string()
                print(f"Decoded course_id: {course_id}, student: {student}")
                print(self.university_dao.enroll_student(course_id, student))
            elif opcode == "03":  # ISSUE_CERTIFICATE
                course_id = self.decode_int()
                student = self.decode_string()
                print(f"Decoded course_id: {course_id}, student: {student}")
                print(self.university_dao.issue_certificate(course_id, student))
            elif opcode == "04":  # VERIFY_CERTIFICATE
                course_id = self.decode_int()
                student = self.decode_string()
                print(f"Decoded course_id: {course_id}, student: {student}")
                print(self.university_dao.verify_certificate(course_id, student))
        print("Bytecode execution completed.")

    def decode_string(self):
        if not self.memory:
            raise IndexError("Memory is empty while decoding string")
        length = int(self.memory.pop(0), 16)
        print(f"String length: {length}")
        if length > len(self.memory):
            raise IndexError(f"Insufficient memory for string of length {length}")
        decoded_string = ''.join([chr(int(self.memory.pop(0), 16)) for _ in range(length)])
        print(f"Decoded string: {decoded_string}")
        return decoded_string

    def decode_int(self):
        if not self.memory:
            raise IndexError("Memory is empty while decoding integer")
        decoded_int = int(self.memory.pop(0), 16)
        print(f"Decoded integer: {decoded_int}")
        return decoded_int

# Example usage
if __name__ == "__main__":
    university_dao = UniversityDAO()
    compiler = CustomCompiler()

    contract_methods = [
        {"name": "CREATE_COURSE", "args": ["Intro to Blockchain", "Dr. Smith"]},
        {"name": "ENROLL_STUDENT", "args": [1, "Alice"]},
        {"name": "ISSUE_CERTIFICATE", "args": [1, "Alice"]},
        {"name": "VERIFY_CERTIFICATE", "args": [1, "Alice"]}
    ]

    bytecode = compiler.compile(contract_methods)
    print(f"Compiled Bytecode: {bytecode}")

    # Correct memory initialization
    vm = CustomVM(university_dao)
    vm.memory = [
        "13", "49", "6e", "74", "72", "6f", "20", "74", "6f", "20", "42", "6c", "6f", "63", "6b", "63", "68", "61", "69", "6e", 
        "09", "44", "72", "2e", "20", "53", "6d", "69", "74", "68", 
        "01", 
        "05", "41", "6c", "69", "63", "65",
        "01",  # Course ID for ISSUE_CERTIFICATE and VERIFY_CERTIFICATE
        "05", "41", "6c", "69", "63", "65"  # Student name for ISSUE_CERTIFICATE and VERIFY_CERTIFICATE
    ]
    vm.execute(bytecode)
