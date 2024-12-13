import re

tokens = {
    'IF': r'IF',
    'LET': r'LET',
    'LOOP': r'LOOP',
    'CALL': r'CALL',
    'IO': r'IO',
    'TRY': r'TRY',
    'MEM': r'MEM',
    'THREAD': r'THREAD',
    'GET': r'GET',
    'SET': r'SET',
    'NUMBER': r'\d+',
    'STRING': r'"[^"]*"',
    'IDENTIFIER': r'[a-zA-Z_]\w*',
    'OPERATOR': r'[+\-*/]',
    'ASSIGN': r'='
}

def tokenize(code):
    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens.items())
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        yield kind, value

code = 'LET x = 10 IF x > 5 CALL IO'
tokens = list(tokenize(code))
print(tokens)


class ASTNode:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

def parse(tokens):
    pos = 0
    
    def parse_expression():
        nonlocal pos
        token_type, token_value = tokens[pos]
        pos += 1
        if token_type == 'NUMBER':
            return ASTNode('NUMBER', int(token_value))
        elif token_type == 'STRING':
            return ASTNode('STRING', token_value.strip('"'))
        # Add more parsing rules here
    
    ast = ASTNode('PROGRAM')
    while pos < len(tokens):
        node = parse_expression()
        ast.children.append(node)
    
    return ast

ast = parse(tokens)
print(ast)

def semantic_analysis(ast):
    # Add semantic checks here
    pass

semantic_analysis(ast)

def generate_code(ast):
    code = []
    
    def visit(node):
        if node.type == 'NUMBER':
            code.append(f'LOAD {node.value}')
        elif node.type == 'STRING':
            code.append(f'LOAD "{node.value}"')
        # Add more code generation rules here
    
    for child in ast.children:
        visit(child)
    
    return code

cryptoleq_code = generate_code(ast)
print(cryptoleq_code)

class Cryptoleq:
    # (existing implementation)

    def load_program_from_code(self, code):
        # Convert code to memory instructions
        self.memory = [self.convert_instruction(instr) for instr in code]

    def convert_instruction(self, instr):
        # Convert human-readable instructions to numeric values
        return 0  # Placeholder implementation

cryptoleq = Cryptoleq(N)
cryptoleq.load_program_from_code(cryptoleq_code)
cryptoleq.execute()
print(cryptoleq.memory)

