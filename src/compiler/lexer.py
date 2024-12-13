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
    tokens.update({'IF', 'LET', 'LOOP', 'DEF', 'IO', 'TRY', 'MEM', 'THREAD', 'GET', 'SET', 'MAT'})

    @_(r'IF')
    def IF(self, t):
        t.type = 'IF'
        return t

    @_(r'LET')
    def LET(self, t):
        t.type = 'LET'
        return t

    @_(r'LOOP')
    def LOOP(self, t):
        t.type = 'LOOP'
        return t

    @_(r'DEF')
    def DEF(self, t):
        t.type = 'DEF'
        return t

    @_(r'IO')
    def IO(self, t):
        t.type = 'IO'
        return t

    @_(r'TRY')
    def TRY(self, t):
        t.type = 'TRY'
        return t

    @_(r'MEM')
    def MEM(self, t):
        t.type = 'MEM'
        return t

    @_(r'THREAD')
    def THREAD(self, t):
        t.type = 'THREAD'
        return t

    @_(r'GET')
    def GET(self, t):
        t.type = 'GET'
        return t

    @_(r'SET')
    def SET(self, t):
        t.type = 'SET'
        return t

    @_(r'MAT')
    def MAT(self, t):
        t.type = 'MAT'
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
