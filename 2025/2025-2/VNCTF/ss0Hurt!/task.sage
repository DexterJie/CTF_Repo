from Crypto.Util.number import *
from flag import flag

class DaMie:
    def __init__(self, flag , n = None):
        self.m = ZZ(bytes_to_long(flag))
        self.n = n if n else getPrime(1024)
        self.P = Zmod(self.n)
        print(f'n = {self.n}')

    def process(self, x, y, z):

        return vector([5 * x + y - 5 * z, 5 * y - z, 5 * z])

    def Mat(self, m):
        PR = self.P['x,y,z']
        x,y,z = PR.gens()

        if m != 0:
            plana = self.Mat(m//2)
            planb = plana(*plana)
            if m % 2 == 0:
                return planb
            else:
                return self.process(*planb)
        else:
            return self.process(*PR.gens())

    def hash(self, A, B, C):
        return self.Mat(self.m)(A, B, C)

if __name__ == '__main__':
    
    Ouch = DaMie(flag)
    result = Ouch.hash(2025,208,209)
    print(f'hash(A,B,C) = {result}')