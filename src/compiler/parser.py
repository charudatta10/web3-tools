from sly import Parser

class MyParser(Parser):
    tokens = MyLexer.tokens

    def __init__(self):
        self.names = {}

    @_('LET IDENTIFIER ASSIGN NUMBER')
    def statement(self, p):
        return ('let', p.IDENTIFIER, p.NUMBER)

    @_('IF condition statement')
    def statement(self, p):
        return ('if', p.condition, p.statement)

    @_('LOOP condition statement')
    def statement(self, p):
        return ('loop', p.condition, p.statement)

    @_('CALL IDENTIFIER statement')
    def statement(self, p):
        return ('function_def', p.IDENTIFIER, p.statement)

    @_('IDENTIFIER')
    def statement(self, p):
        return ('function_call', p.IDENTIFIER)

    @_('IO IDENTIFIER STRING')
    def statement(self, p):
        return ('io', p.IDENTIFIER, p.STRING)

    @_('TRY statement')
    def statement(self, p):
        return ('try', p.statement)

    @_('MEM IDENTIFIER')
    def statement(self, p):
        return ('mem', p.IDENTIFIER)

    @_('THREAD statement')
    def statement(self, p):
        return ('thread', p.statement)

    @_('GET IDENTIFIER')
    def statement(self, p):
        return ('get', p.IDENTIFIER)

    @_('SET IDENTIFIER NUMBER')
    def statement(self, p):
        return ('set', p.IDENTIFIER, p.NUMBER)

    @_('MAT IDENTIFIER')
    def statement(self, p):
        return ('mat', p.IDENTIFIER)

    @_('LPAREN IDENTIFIER COMPARE NUMBER RPAREN')
    def condition(self, p):
        return ('condition', p.IDENTIFIER, p.COMPARE, p.NUMBER)

    @_('condition LOGICAL condition')
    def condition(self, p):
        return ('logical', p.condition0, p.LOGICAL, p.condition1)

    def error(self, p):
        if p:
            print(f'Syntax error at token {p.type!r}')
            self.errok()
        else:
            print('Syntax error at EOF')

if __name__ == "__main__":
    lexer = MyLexer()
    parser = MyParser()
    code = '''
    LET x = 10
    IF (x > 5) && (x < 20)
        CALL myFunction
    MAT tableName
    CALL IO read "input.txt"
    TRY
        CALL riskyFunction
    MEM load x
    THREAD
        CALL parallelFunction
    GET key
    SET key 42
    myFunction
        LET y = 20
        IO write "output.txt"
    '''
    tokens = lexer.tokenize(code)
    ast = parser.parse(tokens)
    print(ast)
