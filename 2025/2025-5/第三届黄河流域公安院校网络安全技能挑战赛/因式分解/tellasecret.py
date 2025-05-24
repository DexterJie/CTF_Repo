import string

from secret import hint
from secret import encrypt

import random

dicts = string.ascii_lowercase +"{=}"

key = (''.join([random.choice(dicts) for i in range(4)])) * 8

assert(len(hint) == 32)

assert(len(key) == 32)


cipher = encrypt(hint, key)    #Vigenere

print(cipher)

# cp=wmaunapgimjfpopeblvup=aywqygb
