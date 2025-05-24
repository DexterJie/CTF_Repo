#!/usr/bin/env python
# Simplify the problem by happy4321
import os, utils
flag = b'flag{' + b'aslfkjasfncioahajsfkjncjkahfahsfklaafafadsf' + b'}'
assert flag.startswith(b'flag{') and flag.endswith(b'}')

seed = int(os.urandom(16).hex(), 16)
gen = utils.Gen(seed)
msg = b'Happy4321: ' + flag
enc = bytes(m ^ next(gen) for m in msg).hex()
print(enc)
# cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48
