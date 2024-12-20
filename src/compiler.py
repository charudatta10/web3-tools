import re

class Lexer:
    def __init__(self):
        self.token_specification = [
            ('NUMBER',   r'\d+'),           # Integer
            ('REGISTER', r'R\d+'),          # Register
            ('OP',       r'[A-Z]+'),        # Operation
            ('COMMA',    r','),             # Comma
            ('SKIP',     r'[ \t]+'),        # Skip over spaces and tabs
            ('MISMATCH', r'.'),             # Any other character
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

    def tokenize(self, code):
        tokens = []
        for mo in re.finditer(self.token_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'REGISTER':
                value = int(value[1:])  # Remove 'R' and convert to integer
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line}')
            tokens.append((kind, value))
        return tokens

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.instructions = []

    def parse_line(self, line):
        tokens = self.lexer.tokenize(line.strip())
        if not tokens:
            return
        instr = tokens[0][1]
        operands = [token[1] for token in tokens[1:] if token[0] != 'COMMA']
        self.instructions.append((instr, operands))

    def parse(self, source_code):
        for line in source_code.splitlines():
            self.parse_line(line)

    def get_instructions(self):
        return self.instructions

class Compiler:
    def __init__(self):
        self.opcode_map = {
            "ADD": 0,
            "SUB": 1,
            "MUL": 2,
            "DIV": 3,
            "AND": 4,
            "OR": 5,
            "XOR": 6,
            "NOT": 7,
            "LOAD": 8,
            "STORE": 9,
            "MOVE": 10,
            "JMP": 11,
            "JZ": 12,
            "JNZ": 13,
            "CALL": 14,
            "RET": 15,
            "HASH": 16,
            "SIGN": 17,
            "VERIFY": 18,
            "BLOCKINFO": 19,
        }

    def compile_instruction(self, instruction):
        instr, operands = instruction
        opcode = self.opcode_map[instr]
        return [opcode] + operands

    def compile(self, instructions):
        compiled_program = []
        for instruction in instructions:
            compiled_program.extend(self.compile_instruction(instruction))
        return compiled_program

if __name__ == "__main__":
    source_code = """
    ADD R1, R2
    SUB R1, R2
    MUL R1, R2
    DIV R1, R2
    """

    lexer = Lexer()
    parser = Parser(lexer)
    parser.parse(source_code)
    instructions = parser.get_instructions()

    compiler = Compiler()
    compiled_program = compiler.compile(instructions)
    print(compiled_program)
