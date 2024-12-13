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
    ('SKIP', r'[ \t]+'),  # Skip whitespace
    ('MISMATCH', r'.'),  # Catch any other character
]

# Compile the regex patterns
token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
get_token = re.compile(token_regex).match

class Lexer:
    def __init__(self, code):
        self.code = code
        self.line = 1
        self.position = 0

    def tokenize(self):
        tokens = []
        mo = get_token(self.code)
        while mo is not None:
            typ = mo.lastgroup
            if typ == 'SKIP':
                pass
            elif typ == 'MISMATCH':
                raise RuntimeError(f'Unexpected character: {mo.group()} at line {self.line}')
            else:
                value = mo.group(typ)
                tokens.append(Token(typ, value, self.position))
            self.position = mo.end()
            mo = get_token(self.code, self.position)
        return tokens

# Example usage
code = 'LET x = 10 IF (x > 5) && (x < 20) CALL IO'
lexer = Lexer(code)
tokens = lexer.tokenize()
for token in tokens:
    print(token)
