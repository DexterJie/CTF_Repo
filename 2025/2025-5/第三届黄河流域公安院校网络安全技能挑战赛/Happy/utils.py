class Gen:
    def __init__(self, state):
        self.nbits = 128
        self.state = state & ((1 << self.nbits) - 1)
        self.mask = 109908700282042807039366676242995409413


    def func0(self, steps=1):
        for _ in range(steps):
            res = self.state & self.mask
            bit = sum([(res >> i) & 1 for i in range(self.nbits)]) & 1
            self.state = ((self.state << 1) ^ bit) & ((1 << self.nbits) - 1)
        return bit

    def __next__(self):
        out = 0
        for _ in range(8):
            bit = self.func0(2023)
            out = (out << 1) ^ bit
        return out