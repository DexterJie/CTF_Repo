from Crypto.Util.number import *
import random
import string
 
def get_flag(length):
    characters = string.ascii_letters + string.digits + '_'
    flag = 'LitCTF{' + ''.join(random.choice(characters) for _ in range(length)) + '}'
    return flag.encode()

flag = get_flag(8)
print(flag)
flag = bin(bytes_to_long(flag))[2:]

p = getPrime(128)
pubkey = [getPrime(128) for i in range(len(flag))]
enc = 0
for i in range(len(flag)):
    enc += pubkey[i] * int(flag[i])
    enc %= p
f = open("output.txt","w")
f.write(f"p = {p}\n")
f.write(f"pubkey = {pubkey}\n")
f.write(f"enc = {enc}\n")
f.close()
