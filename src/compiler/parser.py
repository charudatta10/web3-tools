from lexer import MyLexer
from sly import Parser

class MyParser(Parser):
    tokens = MyLexer.tokens

    @_('statement_list')
    def program(self, p):
        return p.statement_list

    @_('statement statement_list')
    def statement_list(self, p):
        return ('statement_list', p.statement, p.statement_list)

    @_('statement')
    def statement_list(self, p):
        return ('statement_block', p.statement)

    @_('LET IDENTIFIER ASSIGN NUMBER')
    def statement(self, p):
        return ('let', p.IDENTIFIER, p.NUMBER)

    @_('IF condition statement_block')
    def statement(self, p):
        return ('if', p.condition, p.statement_block)

    @_('LOOP condition statement_block')
    def statement(self, p):
        return ('loop', p.condition, p.statement_block)

    @_('DEF IDENTIFIER statement_block')
    def statement(self, p):
        return ('function_def', p.IDENTIFIER, p.statement_block)

    @_('IDENTIFIER')
    def statement(self, p):
        return ('function_call', p.IDENTIFIER)

    @_('IO IDENTIFIER STRING')
    def statement(self, p):
        return ('io', p.IDENTIFIER, p.STRING)

    @_('TRY statement_block')
    def statement(self, p):
        return ('try', p.statement_block)

    @_('MEM IDENTIFIER')
    def statement(self, p):
        return ('mem', p.IDENTIFIER)

    @_('THREAD statement_block')
    def statement(self, p):
        return ('thread', p.statement_block)

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

    @_('statement_list')
    def statement_block(self, p):
        return p.statement_list

    def error(self, p):
        if p:
            print(f'Syntax error at token {p.type!r} at line {p.lineno} index {p.index}')
            self.errok()
        else:
            print('Syntax error at EOF')

if __name__ == "__main__":
    lexer = MyLexer()
    parser = MyParser()
    code = '''
    LET x = 10
    IF (x > 5) && (x < 20)
        DEF myFunction
    MAT tableName
    DEF IO read "input.txt"
    TRY
        DEF riskyFunction
    MEM load x
    THREAD
        DEF parallelFunction
    GET key
    SET key 42

    myFunction
        LET y = 20
        IO write "output.txt"
    '''
    tokens = lexer.tokenize(code)
    tokens = iter(tokens)  # Convert list of tokens to an iterator
    ast = parser.parse(tokens)
    print(ast)
