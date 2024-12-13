from lexer import MyLexer
from parser import MyParser
from code_generator import CodeGenerator
from cryptoleq import Cryptoleq


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

# Run lexer, parser, and code generator
lexer = MyLexer()
tokens = lexer.tokenize(code)
parser = MyParser()
ast = parser.parse(tokens)
code_generator = CodeGenerator()
generated_code = code_generator.generate(ast)
print('\n'.join(generated_code))

# Load and execute generated code on Cryptoleq VM
cryptoleq = Cryptoleq(11)
cryptoleq.load_program_from_code(generated_code)
cryptoleq.execute()
print(cryptoleq.memory)
