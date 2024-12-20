import logging
from compiler import Compiler, Parser, Lexer
from MISA_VM import CustomVM as VM

logging.basicConfig(level=logging.DEBUG)

def main():
    source_code = """
    ADD R1, R2
    SUB R1, R2
    MUL R1, R2
    ADD R1, R2
    SUB R1, R2
    MUL R1, R2
    """

    lexer = Lexer()
    parser = Parser(lexer)
    parser.parse(source_code)
    instructions = parser.get_instructions()

    compiler = Compiler()
    compiled_program = compiler.compile(instructions)
    
    # Print the compiled program for debugging
    print(compiled_program)

    memory = [0] * 1024  # Ensure the memory is large enough
    memory[:len(compiled_program)] = compiled_program

    vm = VM(memory)

    # Initialize registers with values from 1 to 10
    for i in range(10):
        vm.registers[i] = i + 1
    print(vm.registers)
    try:
        vm.execute()
    except Exception as e:
        logging.error(f"Execution failed: {e}")

    logging.debug(f"Final register state: {vm.registers}")
    logging.debug(f"Final memory state: {vm.memory}")

if __name__ == "__main__":
    main()
