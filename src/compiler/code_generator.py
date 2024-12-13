class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0

    def generate(self, node):
        if node is None:
            raise Exception('AST node is None. Check parsing process.')
        print("Generating code for node:", node)  # Debugging line
        method_name = 'gen_' + node[0]
        method = getattr(self, method_name, self.gen_default)
        return method(node)

    def gen_default(self, node):
        raise Exception(f'No generate method for {node[0]}')

    def gen_let(self, node):
        identifier, value = node[1], node[2]
        self.code.append(f'LET {identifier} = {value}')

    def gen_if(self, node):
        condition, body = node[1], node[2]
        self.generate(condition)
        label = self.new_label()
        self.code.append(f'JMP_IF_FALSE {label}')
        self.generate(body)
        self.code.append(f'{label}:')

    def gen_loop(self, node):
        condition, body = node[1], node[2]
        start_label = self.new_label()
        end_label = self.new_label()
        self.code.append(f'{start_label}:')
        self.generate(condition)
        self.code.append(f'JMP_IF_FALSE {end_label}')
        self.generate(body)
        self.code.append(f'JMP {start_label}')
        self.code.append(f'{end_label}:')

    def gen_function_def(self, node):
        func_name = node[1]
        body = node[2]
        self.code.append(f'FUNCTION {func_name}')
        self.generate(body)
        self.code.append(f'END FUNCTION')

    def gen_function_call(self, node):
        func_name = node[1]
        self.code.append(f'CALL {func_name}')

    def gen_io(self, node):
        operation, filename = node[1], node[2]
        self.code.append(f'IO {operation} {filename}')

    def gen_try(self, node):
        body = node[1]
        self.code.append('TRY')
        self.generate(body)
        self.code.append('END TRY')

    def gen_mem(self, node):
        op = node[1]
        self.code.append(f'MEM {op}')

    def gen_thread(self, node):
        body = node[1]
        self.code.append('THREAD')
        self.generate(body)
        self.code.append('END THREAD')

    def gen_get(self, node):
        key = node[1]
        self.code.append(f'GET {key}')

    def gen_set(self, node):
        key, value = node[1], node[2]
        self.code.append(f'SET {key} {value}')

    def gen_mat(self, node):
        table_name = node[1]
        self.code.append(f'MAT {table_name}')

    def gen_condition(self, node):
        left, op, right = node[1], node[2], node[3]
        self.code.append(f'IF {left} {op} {right}')

    def gen_logical(self, node):
        left_condition = node[1]
        logical_op = node[2]
        right_condition = node[3]
        self.generate(left_condition)
        self.code.append(f'{logical_op}')
        self.generate(right_condition)

    def gen_statement_list(self, node):
        self.generate(node[1])
        self.generate(node[2])

    def new_label(self):
        label = f'L{self.label_count}'
        self.label_count += 1
        return label

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
    tokens = iter(tokens)  # Convert list of tokens to an iterator
    ast = parser.parse(tokens)
    print(ast)

    code_generator = CodeGenerator()
    generated_code = code_generator.generate(ast)
    print('\n'.join(generated_code))
