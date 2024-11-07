class CustomCompiler:
    def __init__(self):
        self.instructions = {
            "NOP": "00",
            "LOAD": "01",
            "STORE": "02",
            "ADD": "03",
            "SUB": "04",
            "MUL": "05",
            "DIV": "06",
            "JMP": "07",
            "JZ": "08",
            "HALT": "09"
        }

    def compile(self, abi):
        bytecode = ""
        for func in abi:
            name = func['name'].upper()
            bytecode += self.instructions.get(name, "00")  # Default to NOP if instruction not found
            for input in func['inputs']:
                if input['type'].startswith('uint'):
                    bytecode += f"{int(input['type'][4:]):02x}"  # Handle 'uint256' etc.
                else:
                    bytecode += "00"  # Default encoding for unsupported types
        return bytecode

# Example usage
if __name__ == "__main__":
    abi = [
        {"name": "LOAD", "inputs": [{"type": "uint256"}]},
        {"name": "ADD", "inputs": []},
        {"name": "STORE", "inputs": [{"type": "uint256"}]}
    ]
    compiler = CustomCompiler()
    bytecode = compiler.compile(abi)
    print(f"Compiled Bytecode: {bytecode}")
