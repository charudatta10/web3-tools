class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0

    def generate(self, node):
        method_name = 'gen_' + node.type.lower()
        method = getattr(self, method_name, self.gen_default)
        return method(node)

    def gen_default(self, node):
        raise Exception(f'No generate method for {node.type}')

    def gen_program(self, node):
        for child in node.children:
            self.generate(child)
        return self.code

    def gen_let(self, node):
        identifier, value = node.value
        self.code.append(f'LET {identifier.value} = {value.value}')

    def gen_if(self, node):
        condition, body = node.children
        self.generate(condition)
        label = self.new_label()
        self.code.append(f'JMP_IF_FALSE {label}')
        self.generate(body)
        self.code.append(f'{label}:')

    def gen_loop(self, node):
        condition, body = node.children
        start_label = self.new_label()
        end_label = self.new_label()
        self.code.append(f'{start_label}:')
        self.generate(condition)
        self.code.append(f'JMP_IF_FALSE {end_label}')
        self.generate(body)
        self.code.append(f'JMP {start_label}')
        self.code.append(f'{end_label}:')

    def gen_function_def(self, node):
        func_name = node.value
        body = node.children[0]
        self.code.append(f'FUNCTION {func_name}')
        self.generate(body)
        self.code.append(f'END FUNCTION')

    def gen_function_call(self, node):
        func_name = node.value
        self.code.append(f'CALL {func_name}')

    def gen_io(self, node):
        operation, filename = node.value
        self.code.append(f'IO {operation} {filename}')

    def gen_try(self, node):
        body = node.children[0]
        self.code.append('TRY')
        self.generate(body)
        self.code.append('END TRY')

    def gen_mem(self, node):
        op = node.value
        self.code.append(f'MEM {op}')

    def gen_thread(self, node):
        body = node.children[0]
        self.code.append('THREAD')
        self.generate(body)
        self.code.append('END THREAD')

    def gen_get(self, node):
        key = node.value
        self.code.append(f'GET {key}')

    def gen_set(self, node):
        key, value = node.value
        self.code.append(f'SET {key} {value.value}')

    def gen_mat(self, node):
        table_name = node.value
        self.code.append(f'MAT {table_name}')

    def gen_condition(self, node):
        left, op, right = node.value
        self.code.append(f'IF {left.value} {op.value} {right.value}')

    def gen_logical(self, node):
        left_condition = node.children[0]
        logical_op = node.value
        right_condition = node.children[1]
        self.generate(left_condition)
        self.code.append(f'{logical_op}')
        self.generate(right_condition)

    def new_label(self):
        label = f'L{self.label_count}'
        self.label_count += 1
        return label

# Example usage
if __name__ == "__main__":
    code_generator = CodeGenerator()
    generated_code = code_generator.generate(ast)
    print('\n'.join(generated_code))
