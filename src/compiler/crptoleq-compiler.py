import re
from collections import namedtuple

# Define the token structure
Token = namedtuple('Token', ['type', 'value', 'position'])

# Define token types and patterns
TOKEN_SPECIFICATION = [
    ('NUMBER', r'\d+'),
    ('STRING', r'"[^"]*"'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('ASSIGN', r'='),
    ('OPERATOR', r'[+\-*/]'),
    ('COMPARE', r'[<>]=?|==|!='),
    ('LOGICAL', r'&&|\|\|'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('IF', r'IF'),
    ('LET', r'LET'),
    ('LOOP', r'LOOP'),
    ('CALL', r'CALL'),
    ('IO', r'IO'),
    ('TRY', r'TRY'),
    ('MEM', r'MEM'),
    ('THREAD', r'THREAD'),
    ('GET', r'GET'),
    ('SET', r'SET'),
    ('MAT', r'MAT'),  # New keyword for table data structure
    ('SKIP', r'[ \t]+'),  # Skip whitespace
    ('NEWLINE', r'\n'),   # Line endings
    ('MISMATCH', r'.'),  # Catch any other character
]

# Compile the regex patterns
token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
get_token = re.compile(token_regex).match

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0

    def tokenize(self):
        tokens = []
        line_number = 1
        line_start = 0
        mo = get_token(self.code)
        while mo is not None:
            typ = mo.lastgroup
            value = mo.group(typ)
            if typ == 'NEWLINE':
                line_number += 1
                line_start = mo.end()
            elif typ != 'SKIP':
                column = mo.start() - line_start
                tokens.append(Token(typ, value, (line_number, column)))
            self.position = mo.end()
            mo = get_token(self.code, self.position)
        return tokens

# Example usage
code = 'LET x = 10 IF (x > 5) && (x < 20) MAT table CALL IO'
lexer = Lexer(code)
tokens = lexer.tokenize()
for token in tokens:
    print(token)

class ASTNode:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

    def __repr__(self):
        return f'ASTNode(type={self.type}, value={self.value}, children={self.children})'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        ast = ASTNode('PROGRAM')
        while self.pos < len(self.tokens):
            node = self.parse_expression()
            ast.children.append(node)
        return ast

    def parse_expression(self):
        token = self.tokens[self.pos]
        if token.type == 'LET':
            return self.parse_let()
        elif token.type == 'IF':
            return self.parse_if()
        elif token.type == 'LOOP':
            return self.parse_loop()
        elif token.type == 'CALL':
            return self.parse_call()
        elif token.type == 'IO':
            return self.parse_io()
        elif token.type == 'TRY':
            return self.parse_try()
        elif token.type == 'MEM':
            return self.parse_mem()
        elif token.type == 'THREAD':
            return self.parse_thread()
        elif token.type == 'GET' or token.type == 'SET':
            return self.parse_blockchain_op()
        elif token.type == 'MAT':
            return self.parse_mat()
        else:
            raise SyntaxError(f'Unexpected token: {token.type} at {token.position}')

    def parse_let(self):
        self.expect('LET')
        identifier = self.expect('IDENTIFIER')
        self.expect('ASSIGN')
        value = self.expect('NUMBER')
        return ASTNode('LET', value=[identifier, value])

    def parse_if(self):
        self.expect('IF')
        condition = self.parse_condition()
        body = self.parse_expression()
        node = ASTNode('IF')
        node.children.append(condition)
        node.children.append(body)
        return node

    def parse_loop(self):
        self.expect('LOOP')
        condition = self.parse_condition()
        body = self.parse_expression()
        node = ASTNode('LOOP')
        node.children.append(condition)
        node.children.append(body)
        return node

    def parse_call(self):
        self.expect('CALL')
        func_name = self.expect('IDENTIFIER')
        node = ASTNode('CALL', func_name.value)
        return node

    def parse_io(self):
        self.expect('IO')
        op = self.expect('IDENTIFIER')
        node = ASTNode('IO', op.value)
        return node

    def parse_try(self):
        self.expect('TRY')
        body = self.parse_expression()
        node = ASTNode('TRY')
        node.children.append(body)
        return node

    def parse_mem(self):
        self.expect('MEM')
        op = self.expect('IDENTIFIER')
        node = ASTNode('MEM', op.value)
        return node

    def parse_thread(self):
        self.expect('THREAD')
        body = self.parse_expression()
        node = ASTNode('THREAD')
        node.children.append(body)
        return node

    def parse_blockchain_op(self):
        token = self.tokens[self.pos]
        if token.type == 'GET':
            self.expect('GET')
            key = self.expect('IDENTIFIER')
            return ASTNode('GET', key.value)
        elif token.type == 'SET':
            self.expect('SET')
            key = self.expect('IDENTIFIER')
            value = self.expect('NUMBER')
            return ASTNode('SET', value=[key.value, value])

    def parse_mat(self):
        self.expect('MAT')
        table_name = self.expect('IDENTIFIER')
        return ASTNode('MAT', table_name.value)

    def parse_condition(self):
        self.expect('LPAREN')
        left = self.expect('IDENTIFIER')
        op = self.expect('COMPARE')
        right = self.expect('NUMBER')
        self.expect('RPAREN')
        return ASTNode('CONDITION', value=[left, op, right])

    def expect(self, expected_type):
        token = self.tokens[self.pos]
        if token.type == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f'Expected token type {expected_type}, got {token.type}')

# Example usage
parser = Parser(tokens)
ast = parser.parse()
print(ast)

def generate_code(ast):
    code = []

    def visit(node):
        if node.type == 'LET':
            identifier, value = node.value
            code.append(f'LET {identifier.value} = {value.value}')
        elif node.type == 'IF':
            condition, body = node.children
            code.append(f'IF ({condition.children[0].value} {condition.children[1].value} {condition.children[2].value})')
            visit(body)
        elif node.type == 'LOOP':
            condition, body = node.children
            code.append(f'LOOP ({condition.children[0].value} {condition.children[1].value} {condition.children[2].value})')
            visit(body)
        elif node.type == 'CALL':
            code.append(f'CALL {node.value}')
        elif node.type == 'IO':
            code.append(f'IO {node.value}')
        elif node.type == 'TRY':
            code.append('TRY')
            visit(node.children[0])
        elif node.type == 'MEM':
            code.append(f'MEM {node.value}')
        elif node.type == 'THREAD':
            code.append('THREAD')
            visit(node.children[0])
        elif node.type == 'GET':
            code.append(f'GET {node.value}')
        elif node.type == 'SET':
            key, value = node.value
            code.append(f'SET {key} = {value.value}')
        elif node.type == 'MAT':
            code.append(f'MAT {node.value}')
        # Add other node types as needed

    visit(ast)
    return code

cryptoleq_code = generate_code(ast)
print(cryptoleq_code)
