# SageMath 10.6
from sage.all import *

def Knapsack_Lattice1_LLL_attack_without_mod(pk,S):
    candidate_sulotions = []
    n = len(pk)
    d = n / log(max(pk),2)
    # print(f"背包密度为: {CDF(d)}")
    
    Ge = Matrix(ZZ,n+1,n+1)
    for i in range(n):
        Ge[i,i] = 1
        Ge[i,-1] = pk[i]
    Ge[-1,-1] = S
    N = ceil(sqrt(n))
    Ge[:,-1] *= N
    for line in Ge.LLL():
        if set(line[:-1]).issubset({0,1}):
            m = ''
            for i in line[:-1]:
                if i == 1:
                    m += '1'
                if i == 0:
                    m += '0'
            candidate_sulotions.append(m)
        if set(line[:-1]).issubset({0,-1}):
            m = ''
            for i in line[:-1]:
                if i == -1:
                    m += '1'
                if i == 0:
                    m += '0'
            candidate_sulotions.append(m)
    return candidate_sulotions

def Knapsack_Lattice1_BKZ_attack_without_mod(pk,S):
    candidate_sulotions = []
    n = len(pk)
    d = n / log(max(pk),2)
    # print(f"背包密度为: {CDF(d)}")
    
    Ge = Matrix(ZZ,n+1,n+1)
    for i in range(n):
        Ge[i,i] = 1
        Ge[i,-1] = pk[i]
    Ge[-1,-1] = S
    for line in Ge.BKZ():
        if set(line[:-1]).issubset({0,1}):
            m = ''
            for i in line[:-1]:
                if i == 1:
                    m += '1'
                if i == 0:
                    m += '0'
            candidate_sulotions.append(m)
        if set(line[:-1]).issubset({0,-1}):
            m = ''
            for i in line[:-1]:
                if i == -1:
                    m += '1'
                if i == 0:
                    m += '0'
            candidate_sulotions.append(m)
    return candidate_sulotions

def Knapsack_Lattice2_LLL_attack_without_mod(pk,S):
    candidate_sulotions = []
    n = len(pk)
    d = n / log(max(pk),2)
    # print(f"背包密度为: {CDF(d)}")
    
    Ge = Matrix(ZZ,n+1,n+1)
    for i in range(n):
        Ge[i,i] = 2
        Ge[-1,i] = 1
        Ge[i,-1] = pk[i]
    Ge[-1,-1] = S
    for line in Ge.LLL():
        if set(line[:-1]).issubset({-1,1}):
            m1 = ''
            m2 = ''
            for i in line[:-1]:
                if i == 1:
                    m1 += '1'
                    m2 += '0'
                if i == -1:
                    m1 += '0'
                    m2 += '1'
            candidate_sulotions.append(m1)
            candidate_sulotions.append(m2)
    return candidate_sulotions

if "__name__" == "__main__":
    from Crypto.Util.number import *
    import random

    for d in range(40,95):
        nums = 500
        count = 0
        for _ in range(nums):
            secret_bits = d
            secret = random.getrandbits(secret_bits)
            M = [getPrime(100) for _ in range(secret_bits)]
            S = 0
            for i in M:
                temp = secret % 2
                S += temp * i
                secret = secret >> 1

            solutions = Knapsack_Lattice1_BKZ_attack_without_mod(M,S)
            if len(solutions) != 0:
                count += 1
                
        print(f"{CDF(d / 100)} : {CDF(count / nums)}")