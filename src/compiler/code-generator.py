class CodeGenerator:
    def __init__(self):
        self.variables = {}
        self.memory = []
        self.IP = 0

    def generate(self, ast):
        for node in ast:
            self.visit(node)
        return self.memory

    def visit(self, node):
        method_name = 'visit_' + node[0]
        visitor = getattr(self, method_name)
        return visitor(node)

    def visit_let(self, node):
        _, var, expr = node
        value = self.evaluate_expression(expr)
        if var not in self.variables:
            self.variables[var] = self.IP
            self.IP += 1
        self.memory.append(self.variables[var])
        self.memory.append(value)
        self.memory.append(self.IP + 3)
        self.IP += 3

    def visit_if(self, node):
        _, condition, body = node
        condition_value = self.evaluate_expression(condition)
        self.memory.append(condition_value)
        self.memory.append(self.IP + 6)
        self.memory.append(self.IP + 3)
        self.IP += 6
        for stmt in body:
            self.visit(stmt)

    def visit_while(self, node):
        _, condition, body = node
        condition_value = self.evaluate_expression(condition)
        start_ip = self.IP
        self.memory.append(condition_value)
        self.memory.append(self.IP + 9)
        self.memory.append(self.IP + 3)
        self.IP += 9
        for stmt in body:
            self.visit(stmt)
        self.memory.append(start_ip)

    def visit_add(self, node):
        _, left, right = node
        left_value = self.evaluate_expression(left)
        right_value = self.evaluate_expression(right)
        self.memory.append(left_value + right_value)
        self.memory.append(self.IP + 3)
        self.memory.append(self.IP + 3)
        self.IP += 3

    def visit_sub(self, node):
        _, left, right = node
        left_value = self.evaluate_expression(left)
        right_value = self.evaluate_expression(right)
        self.memory.append(left_value - right_value)
        self.memory.append(self.IP + 3)
        self.memory.append(self.IP + 3)
        self.IP += 3

    def visit_multiply(self, node):
        _, left, right = node
        left_value = self.evaluate_expression(left)
        right_value = self.evaluate_expression(right)
        self.memory.append(left_value * right_value)
        self.memory.append(self.IP + 3)
        self.memory.append(self.IP + 3)
        self.IP += 3

    def visit_divide(self, node):
        _, left, right = node
        left_value = self.evaluate_expression(left)
        right_value = self.evaluate_expression(right)
        self.memory.append(left_value // right_value)
        self.memory.append(self.IP + 3)
        self.memory.append(self.IP + 3)
        self.IP += 3

    def evaluate_expression(self, expr):
        if expr[0] == 'number':
            return expr[1]
        elif expr[0] == 'var':
            return self.variables