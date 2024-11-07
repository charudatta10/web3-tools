class CustomVM:
    def __init__(self):
        self.memory = {}
        self.instruction_pointer = 0
        self.stack = []

    def execute(self, bytecode):
        while self.instruction_pointer < len(bytecode):
            opcode = bytecode[self.instruction_pointer:self.instruction_pointer + 2]
            self.instruction_pointer += 2
            if opcode == "00":  # NOP
                continue
            elif opcode == "01":  # LOAD
                value = int(bytecode[self.instruction_pointer:self.instruction_pointer + 2], 16)
                self.stack.append(value)
                self.instruction_pointer += 2
            elif opcode == "02":  # STORE
                address = int(bytecode[self.instruction_pointer:self.instruction_pointer + 2], 16)
                self.memory[address] = self.stack.pop()
                self.instruction_pointer += 2
            elif opcode == "03":  # ADD
                self.stack.append(self.stack.pop() + self.stack.pop())
            elif opcode == "09":  # HALT
                break

# Example usage
if __name__ == "__main__":
    bytecode = "01050103050209"
    vm = CustomVM()
    vm.execute(bytecode)
    print(f"Memory: {vm.memory}")
    print(f"Stack: {vm.stack}")
