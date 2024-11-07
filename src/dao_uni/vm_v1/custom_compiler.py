class CustomCompiler:
    def __init__(self):
        self.instructions = {
            "CREATE_COURSE": "01",
            "ENROLL_STUDENT": "02",
            "ISSUE_CERTIFICATE": "03",
            "VERIFY_CERTIFICATE": "04"
        }

    def compile(self, methods):
        bytecode = ""
        for method in methods:
            name = method['name'].upper()
            bytecode += self.instructions.get(name, "00")  # Default to NOP if instruction not found
            for arg in method['args']:
                if isinstance(arg, int):
                    bytecode += f"{arg:02x}"  # Encode integers in hexadecimal
                elif isinstance(arg, str):
                    encoded_string = ''.join(f"{ord(c):02x}" for c in arg)  # Encode strings as ASCII hex
                    length = f"{len(arg):02x}"  # Encode length in hexadecimal (number of characters)
                    bytecode += length + encoded_string  # Concatenate length and encoded string
        return bytecode



# Example usage
if __name__ == "__main__":
    abi = [
        {"name": "CREATE_COURSE", "args": ["Intro to Blockchain", "Dr. Smith"]},
        {"name": "ENROLL_STUDENT", "args": [1, "Alice"]},
        {"name": "ISSUE_CERTIFICATE", "args": [1, "Alice"]},
        {"name": "VERIFY_CERTIFICATE", "args": [1, "Alice"]}
    ]
    compiler = CustomCompiler()
    bytecode = compiler.compile(abi)
    print(f"Compiled Bytecode: {bytecode}")
