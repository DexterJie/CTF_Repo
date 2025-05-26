from secret import flag
from Crypto.Util.number import getPrime, bytes_to_long

assert len(flag) == 64
m1 = bytes_to_long(flag[:32].encode())
m2 = bytes_to_long(flag[32:].encode())

p = getPrime(256)
def release(m):
    print(hex((m * pow(2, m, p)) % p)[2:].rjust(64, '0'))

print(hex(p)[2:])
release(m1)
release(m2)
release(m2-m1)
release(m2+m1)
"""
afe4dfec75d05b8204f949749dce9d69eaee982528f7e2c177862b4f12b635d9
6d04f0ebde78ca72c0a65629cd6f2cc337319c05b266ed789843ea2bdf11551f
61483d050ad72a0e6dda11e3f683fbac20ab17b4a26615ac3eb4fbaecef519bd
13c9395628b7f90ff1675d73cc97ae24ea5c9993366364627d20f9f52b19fabb
75e04f3f38420029fa57934de57b6fb59f9615e4be32eaa4460c57a47c2842ae
"""