import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_token = 0

    def tokenize(self):
        token_specification = [
            ('NUMBER',    r'\d+'),            # Integer
            ('ID',        r'[A-Za-z_]\w*'),   # Identifiers
            ('OP',        r'[+*-/]'),         # Arithmetic operators
            ('LET',       r'let'),            # Variable assignment
            ('IF',        r'if'),             # If keyword
            ('WHILE',     r'while'),          # While keyword
            ('ADD',       r'add'),            # Add keyword
            ('SUB',       r'sub'),            # Subtract keyword
            ('MUL',       r'multiply'),       # Multiply keyword
            ('DIV',       r'divide'),         # Divide keyword
            ('LPAREN',    r'\('),             # Left Parenthesis
            ('RPAREN',    r'\)'),             # Right Parenthesis
            ('EQ',        r'='),              # Assignment operator
            ('COMMENT',   r'#.*'),            # Comment
            ('SKIP',      r'[ \t\n]+'),       # Skip spaces and newlines
            ('MISMATCH',  r'.'),              # Any other character
        ]
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_num = 1
        line_start = 0
        mo = get_token(self.source_code)
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'ID':
                value = value
            elif kind == 'COMMENT' or kind == 'SKIP':
                mo = get_token(self.source_code, mo.end())
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            self.tokens.append((kind, value))
            mo = get_token(self.source_code, mo.end())
        self.tokens.append(('EOF', 'EOF'))
        return self.tokens
