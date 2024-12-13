import math

class Cryptoleq:
    def __init__(self, N):
        self.N = N
        self.memory = []
        self.IP = 0

    def O1(self, x, y):
        N2 = self.N ** 2
        try:
            inv_x = pow(x, -1, N2)
        except ValueError:
            # Handle non-invertible case
            inv_x = 1  # or another appropriate value or handling mechanism
        return (inv_x * y) % N2

    def O2(self, x):
        return math.floor((x - 1) / self.N)

    def load_program(self, program):
        self.memory = program

    def execute(self):
        while self.IP < len(self.memory):
            if self.IP + 2 >= len(self.memory):
                break
            a = self.memory[self.IP]
            b = self.memory[self.IP + 1]
            c = self.memory[self.IP + 2]

            self.memory