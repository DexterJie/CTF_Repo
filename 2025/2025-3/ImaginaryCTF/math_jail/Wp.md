实际测试会发现大概几百次中，100个值里面会出现0个素数。

```py
def isprime(n):
    if n < 2:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

# make sure your solution is memory efficient :)
START = 100_000_000
END   = 1_000_000_000
TESTS = 100
from random import randrange

dic = []
for u in range(1000):
    t = []
    for _ in range(TESTS):
        rand_num = randrange(START, END)
        if isprime(rand_num):
            t.append(rand_num)
    if (len(set(t)) == 0):
        print(t)
```

所以直接让这个`prime_check`每次都返回0，去拼运气

> exp.py

```py
# python 3.11.4
from pwn import *
from tqdm import trange
context.log_level = 'error'

for i in trange(1000):
    sh = remote('155.248.210.243',42179)
    sh.recvuntil(b'Your prime check:')
    sh.sendline(b'n-n')
    rc = sh.recvline()
    sh.close()
    if b"I knew you weren't worthy." not in rc:
        print(sh.recvall().strip().decode())
        # ictf{what?_it_was_gambling_all_along?}
```
