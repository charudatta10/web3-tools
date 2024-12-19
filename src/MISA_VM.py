import logging

logging.basicConfig(level=logging.DEBUG)

class CustomVM:
    def __init__(self, memory):
        self.memory = memory  # Initial memory setup
        self.pc = 0  # Program counter
        self.registers = [0] * 10  # 10 general-purpose registers
        self.stack = []
        self.instructions = {
            0: self.add,
            1: self.sub,
            2: self.mul,
            3: self.div,
            4: self.and_op,
            5: self.or_op,
            6: self.xor_op,
            7: self.not_op,
            8: self.load,
            9: self.store,
            10: self.move,
            11: self.jmp,
            12: self.jz,
            13: self.jnz,
            14: self.call,
            15: self.ret,
            16: self.hash_op,
            17: self.sign,
            18: self.verify,
            19: self.block_info,
        }

    def fetch_instruction(self):
        op_code = self.memory[self.pc]
        self.pc += 1
        return op_code

    def load_program(self, program):
        self.memory.extend(program)

    def execute(self):
        while self.pc < len(self.memory):
            op_code = self.fetch_instruction()
            if op_code in self.instructions:
                self.instructions[op_code]()
            else:
                raise ValueError(f"Unknown instruction {op_code}")

    def validate_register_index(self, index):
        if index < 0 or index >= len(self.registers):
            raise IndexError(f"Register index {index} out of range.")

    def add(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc + 1]
        self.validate_register_index(a)
        self.validate_register_index(b)
        self.registers[a] += self.registers[b]
        self.pc += 2

    def sub(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc + 1]
        if self.validate_register_index(a):
            if self.validate_register_index(b):
                self.registers[a] -= self.registers[b]
        self.pc += 2

    def mul(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc + 1]
        self.validate_register_index(a)
        self.validate_register_index(b)
        self.registers[a] *= self.registers[b]
        self.pc += 2

    def div(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc + 1]
        self.validate_register_index(a)
        self.validate_register_index(b)
        if self.registers[b] == 0:
            logging.error(f"Division by zero error: register[{b}] is zero. Skipping operation.")
        else:
            self.registers[a] //= self.registers[b]
        self.pc += 2

    def and_op(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc + 1]
        if self.validate_register_index(a):
            if self.validate_register_index(b):
                self.registers[a] &= self.registers[b]
        self.pc += 2

    def or_op(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc + 1]
        self.validate_register_index(a)
        self.validate_register_index(b)
        self.registers[a] |= self.registers[b]
        self.pc += 2

    def xor_op(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc + 1]
        self.validate_register_index(a)
        self.validate_register_index(b)
        self.registers[a] ^= self.registers[b]
        self.pc += 2

    def not_op(self):
        a = self.memory[self.pc]
        self.validate_register_index(a)
        self.registers[a] = ~self.registers[a]
        self.pc += 1

    def load(self):
        a = self.memory[self.pc]
        address = self.memory[self.pc + 1]
        self.validate_register_index(a)
        self.registers[a] = self.memory[address]
        self.pc += 2

    def store(self):
        a = self.memory[self.pc]
        address = self.memory[self.pc + 1]
        self.validate_register_index(a)
        self.memory[address] = self.registers[a]
        self.pc += 2

    def move(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc + 1]
        self.validate_register_index(a)
        self.validate_register_index(b)
        self.registers[b] = self.registers[a]
        self.pc += 2

    def jmp(self):
        address = self.memory[self.pc]
        self.pc = address

    def jz(self):
        address = self.memory[self.pc]
        if self.registers[0] == 0:
            self.pc = address
        else:
            self.pc += 1

    def jnz(self):
        address = self.memory[self.pc]
        if self.registers[0] != 0:
            self.pc = address
        else:
            self.pc += 1

    def call(self):
        address = self.memory[self.pc]
        self.stack.append(self.pc + 1)
        self.pc = address

    def ret(self):
        self.pc = self.stack.pop()

    def hash_op(self):
        a = self.memory[self.pc]
        self.validate_register_index(a)
        self.registers[a] = sum(map(ord, str(self.registers[a])))
        self.pc += 1

    def sign(self):
        a = self.memory[self.pc]
        self.validate_register_index(a)
        private_key = "private_key"
        self.registers[a] = hash(self.registers[a] + hash(private_key))
        self.pc += 1

    def verify(self):
        a = self.memory[self.pc]
        self.validate_register_index(a)
        public_key = "public_key"
        self.registers[a] = (self.registers[a] == hash(self.registers[a] + hash(public_key)))
        self.pc += 1

    def block_info(self):
        self.registers[0] = 123456
        self.pc += 1



# Initialize the VM with some memory
initial_memory = [
    0, 1, 2,  # ADD R1, R2
    1, 1, 2,  # SUB R1, R2
    2, 1, 2,  # MUL R1, R2
    3, 1, 2,  # DIV R1, R2 (ensure R2 is not zero)
    11, 4,    # JMP to address 4
    10, 1, 3, # MOVE R1 to R3
]

# Create the VM instance
vm = CustomVM(initial_memory)
vm.execute()

# Output the result
logging.debug(f"Final register state: {vm.registers}")
logging.debug(f"Final memory state: {vm.memory}")
