from Crypto.Util.number import *
from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad
from secret import flag
miku = 30
p = getPrime(512)
key = getPrime(512)
while key> p:
    key= getPrime(512)
ts = []
gs = []
zs = []
for i in range(miku):
    t = getPrime(512)
    z = getPrime(400)
    g= (t * key + z) % p
    ts.append(t)
    gs.append(g)
    zs.append(z)
print(f'p = {p}')
print(f'ts = {ts}')
print(f'gs = {gs}')
iv= os.urandom(16)
cipher = AES.new(str(key).encode()[:16], AES.MODE_CBC,iv)
ciphertext=cipher.encrypt(pad(flag.encode(),16))
print(f'iv={iv}')
print(f'ciphertext={ciphertext}')