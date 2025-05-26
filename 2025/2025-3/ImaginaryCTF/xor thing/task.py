from secrets import randbits
from os import urandom
from secret import flag
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
import json

A = [randbits(64) for _ in range(48)]
a = randbits(48)

b = 0
for i in range(48):
    if (a>>i)%2 == 1:
        b ^= A[i]

hsh = sha256(str(a).encode())
key = hsh.digest()
iv = urandom(16)
cipher = AES.new(key, AES.MODE_CBC, IV=iv)
out = {'A':A, 'b':b, 'c':cipher.encrypt(pad(flag.encode(),16)).hex()+';'+iv.hex()}
print(json.dumps(out))
B = 0
for wild in A:
    B ^= wild