from sly import Lexer

class MyLexer(Lexer):
    tokens = { NUMBER, STRING, IDENTIFIER, ASSIGN, OPERATOR, COMPARE, LOGICAL, LPAREN, RPAREN, IF, LET, LOOP, CALL, IO, TRY, MEM, THREAD, GET, SET, MAT }
    ignore = ' \t'

    # Token patterns
    NUMBER = r'\d+'
    STRING = r'"[^"]*"'
    IDENTIFIER = r'[a-zA-Z_]\w*'
    ASSIGN = r'='
    OPERATOR = r'[+\-*/]'
    COMPARE = r'[<>]=?|==|!='
    LOGICAL = r'&&|\|\|'
    LPAREN = r'\('
    RPAREN = r'\)'

    # Keywords
    IF = r'IF'
    LET = r'LET'
    LOOP = r'LOOP'
    CALL = r'CALL'
    IO = r'IO'
    TRY = r'TRY'
    MEM = r'MEM'
    THREAD = r'THREAD'
    GET = r'GET'
    SET = r'SET'
    MAT = r'MAT'

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
    for token in lexer.tokenize(code):
        print(token)
