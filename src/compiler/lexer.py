from sly import Lexer

class MyLexer(Lexer):
    tokens = { NUMBER, STRING, IDENTIFIER, ASSIGN, COMPARE, LOGICAL, LPAREN, RPAREN, IF, LET, LOOP, DEF, IO, TRY, MEM, THREAD, GET, SET, MAT }
    ignore = ' \t'

    # Token patterns
    NUMBER = r'\d+'
    STRING = r'"[^"]*"'
    IDENTIFIER = r'[a-zA-Z_]\w*'
    ASSIGN = r'='
    COMPARE = r'[<>]=?|==|!='
    LOGICAL = r'&&|\|\|'
    LPAREN = r'\('
    RPAREN = r'\)'

    # Keywords
    keywords = { 'IF', 'LET', 'LOOP', 'DEF', 'IO', 'TRY', 'MEM', 'THREAD', 'GET', 'SET', 'MAT' }

    @_(r'[a-zA-Z_]\w*')
    def IDENTIFIER(self, t):
        if t.value.upper() in self.keywords:
            t.type = t.value.upper()
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f'Illegal character {t.value[0]!r}')
        self.index += 1

if __name__ == "__main__":
    lexer = MyLexer()
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
    for token in lexer.tokenize(code):
        print(token)
