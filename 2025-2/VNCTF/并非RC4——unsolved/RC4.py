from Crypto.Util.number import *
from sympy import *
import random
from secret import small_key, flag

#你能找到这个实现错在哪吗
def faulty_rc4_encrypt(text):
    data_xor_iv = []
    sbox = []
    j = 0
    x = y = k = 0
    key = small_key
    
    for i in range(256):
        sbox.append(i)
    else:
        for i in range(256):
            j = j + sbox[i] + ord(key[i % len(key)]) & 255
            sbox[i] = sbox[j]  
            sbox[j] = sbox[i]
        else:
            for idx in text:
                x = x + 1 & 255
                y = y + sbox[x] & 255
                sbox[x] = sbox[y] 
                sbox[y] = sbox[x]
                k = sbox[sbox[x] + sbox[y] & 255]
                data_xor_iv.append(idx^k^17)
    return data_xor_iv


def main():
    mt_string = bytes([random.getrandbits(8) for _ in range(40000)])
    encrypted_data = faulty_rc4_encrypt(mt_string)
    
    p = nextprime(random.getrandbits(512))
    q = nextprime(random.getrandbits(512))
    n = p * q
    e = 65537
    
    flag_number = bytes_to_long(flag.encode())
    encrypted_flag = pow(flag_number, e, n)
    
    with open("data_RC4.txt", "w") as f:
        f.write(str(encrypted_data))
    
    print("n =", n)
    print("e =", e)
    print("encrypted_flag =", encrypted_flag)
    
if __name__ == "__main__":
    main()


'''
n = 26980604887403283496573518645101009757918606698853458260144784342978772393393467159696674710328131884261355662514745622491261092465745269577290758714239679409012557118030398147480332081042210408218887341210447413254761345186067802391751122935097887010056608819272453816990951833451399957608884115252497940851
e = 65537
encrypted_flag = 22847144372366781807296364754215583869872051137564987029409815879189317730469949628642001732153066224531749269434313483657465708558426141747771243442436639562785183869683190497179323158809757566582076031163900773712582568942616829434508926165117919744857175079480357695183964845638413639130567108300906156467

'''