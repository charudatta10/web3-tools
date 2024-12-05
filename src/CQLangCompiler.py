from src.cryptoleq import Cryptoleq

class CQLangCompiler:
    def __init__(self):
        self.variables = {}
        self.memory = []
        self.IP = 0
        self.function_map = {'foo': 99}  # Example mapping of functions to memory addresses

    def compile(self, program):
        lines = program.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line.startswith("let"):
                self.compile_assignment(line)
            elif line.startswith("if"):
                self.compile_if(line)
            elif line.startswith("while"):
                self.compile_while(line)
            elif line.startswith("call"):
                self.compile_call(line)
        return self.memory

    def compile_assignment(self, line):
        parts = line.split("=")
        var = parts[0].split()[1].strip()
        expr = parts[1].strip()
        expr_value = self.evaluate_expression(expr)
        if var not in self.variables:
            self.variables[var] = self.IP
            self.IP += 1
        # Storing both variable address and its computed value
        self.memory.append(self.variables[var])
        self.memory.append(expr_value)
        self.memory.append(self.IP + 3)
        self.IP += 3

    def evaluate_expression(self, expr):
        try:
            for var in self.variables:
                expr = expr.replace(var, str(self.variables[var]))
            # Evaluate expression considering it might contain variables
            return eval(expr, {}, self.variables)
        except NameError as e:
            raise ValueError(f"Undefined variable in expression: {expr}")

    def compile_if(self, line):
        condition = line.split()[1]
        condition_value = self.evaluate_expression(condition)
        self.memory.append(condition_value)
        self.memory.append(self.IP + 6)
        self.memory.append(self.IP + 3)
        self.IP += 6

    def compile_while(self, line):
        condition = line.split()[1]
        condition_value = self.evaluate_expression(condition)
        start_ip = self.IP
        self.memory.append(condition_value)
        self.memory.append(self.IP + 9)
        self.memory.append(self.IP + 3)
        self.IP += 9
        self.memory.append(start_ip)
    
    def compile_call(self, line):
        func = line.split()[1]
        if func in self.function_map:
            self.memory.append(self.function_map[func])
        else:
            raise ValueError(f"Undefined function: {func}")
        self.memory.append(self.IP + 3)
        self.memory.append(self.IP + 3)
        self.IP += 3

# Example usage
compiler = CQLangCompiler()
cqlang_program = """
# Define variables
let a = 10
let b = 20
let c = 30

# Perform arithmetic operations
let d = a + b * c

# Control flow
if d > 100
    let e = d - 100
else
    let e = d + 100

# Loop
while e < 500
    let e = e + 10

# Call a function
call foo
"""
cryptoleq_program = compiler.compile(cqlang_program)
print(cryptoleq_program)

# Example usage
N = 123457  # Example large prime number
program = cryptoleq_program  # Example program
cryptoleq = Cryptoleq(N)
cryptoleq.load_program(program)
cryptoleq.execute()
print(cryptoleq.memory)
