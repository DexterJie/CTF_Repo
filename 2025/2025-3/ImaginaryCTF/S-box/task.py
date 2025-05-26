from Crypto.Util.number import *
from secrets import randbits


def rc4(key, data):

    S = [randbits(8) for _ in range(256)]
    j = 0

    for idx in range(len(key)):
        i = idx & 0xff
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i] ^= S[j]
        S[j] ^= S[i]
        S[i] ^= S[j]

    i = 0
    j = 0
    output = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i] ^= S[j]
        S[j] ^= S[i]
        S[i] ^= S[j]
        K = S[(S[i] + S[j]) % 256]
        output.append(byte ^ K)
    return bytes(output)


flag = open("flag.txt", "rb").read().strip()
try:
    key = input("🔑 ").encode()
except:
    exit(0)
ciphertext = rc4(key, flag)
print(f"🔒 {ciphertext}")