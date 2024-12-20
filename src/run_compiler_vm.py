import logging
from compiler import Compiler, Parser, Lexer  # Ensure your compiler-related classes are in compiler.py
from MISA_VM import CustomVM  # Ensure your VM-related classes are in vm.py

logging.basicConfig(level=logging.DEBUG)

def main():
    # Define your high-level source code
    source_code = """
    ADD R1, R2
    SUB R1, R2
    MUL R1, R2
    DIV R1, R2
    """

    # Compile the source code
    lexer = Lexer()
    parser = Parser(lexer)
    parser.parse(source_code)
    instructions = parser.get_instructions()

    compiler = Compiler()
    compiled_program = compiler.compile(instructions)

    # Initialize the VM with the compiled program
    memory = [0] * 1024  # Create a memory space large enough to hold the program
    memory[:len(compiled_program)] = compiled_program

    vm = VM(memory)
    vm.execute()

    # Output the result
    logging.debug(f"Final register state: {vm.registers}")
    logging.debug(f"Final memory state: {vm.memory}")

if __name__ == "__main__":
    main()
