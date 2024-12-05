class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token < len(self.tokens) - 1:
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def statement(self):
        token = self.tokens[self.current_token]
        if token[0] == 'LET':
            return self.assignment()
        elif token[0] == 'IF':
            return self.if_statement()
        elif token[0] == 'WHILE':
            return self.while_statement()
        elif token[0] == 'ADD':
            return self.add_statement()
        elif token[0] == 'SUB':
            return self.sub_statement()
        elif token[0] == 'MUL':
            return self.mul_statement()
        elif token[0] == 'DIV':
            return self.div_statement()
        elif token[0] == 'COMMENT':
            self.current_token += 1
            return None
        else:
            raise RuntimeError(f'Unexpected token: {token[1]}')

    def assignment(self):
        self.consume('LET')
        var_name = self.consume('ID')
        self.consume('EQ')
        expr = self.expression()
        return ('let', var_name[1], expr)

    def if_statement(self):
        self.consume('IF')
        condition = self.expression()
        body = self.program()
        return ('if', condition, body)

    def while_statement(self):
        self.consume('WHILE')
        condition = self.expression()
        body = self.program()
        return ('while', condition, body)

    def add_statement(self):
        self.consume('ADD')
        left = self.expression()
        self.consume('ADD')
        right = self.expression()
        return ('add', left, right)

    def sub_statement(self):
        self.consume('SUB')
        left = self.expression()
        self.consume('SUB')
        right = self.expression()
        return ('sub', left, right)

    def mul_statement(self):
        self.consume('MUL')
        left = self.expression()
        self.consume('MUL')
        right = self.expression()
        return ('multiply', left, right)

    def div_statement(self):
        self.consume('DIV')
        left = self.expression()
        self.consume('DIV')
        right = self.expression()
        return ('divide', left, right)

    def expression(self):
        token = self.tokens[self.current_token]
        if token[0] == 'NUMBER':
            self.current_token += 1
            return ('number', token[1])
        elif token[0] == 'ID':
            self.current_token += 1
            return ('var', token[1])
        else:
            raise RuntimeError(f'Unexpected token: {token[1]}')

    def consume(self, token_type):
        token = self.tokens[self.current_token]
        if token[0] == token_type:
            self.current_token += 1
            return token
        else:
            raise RuntimeError(f'Expected {token_type}, but got {token[1]}')
