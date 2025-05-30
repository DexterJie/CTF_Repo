level1：

有两次输入`m`的机会，服务器每次返回`(m | x) + (m | y)`，然后给出一个`m'`，要求我们输入`(m' | x) + (m' | y)`的值，如果和服务器那边计算结果相符就给flag

那思路就很清晰了，用两次自定义`m`的机会计算出`x`和`y`

任意输入两次`m`，将两次返回的结果用z3求解

level2：

同样两次输入`m`的机会，这次返回的是`(m | x) + (m ^ y)`

依旧用z3求解

```py
from pwn import *
from z3 import *

sh = remote('127.0.0.1',2227)

# Level 1
level1_m1 = 0
level1_m2 = int('01'*15,2)
sh.recvuntil(b"Level 1:")
sh.sendlineafter(b"Enter your number: ",str(level1_m1).encode())
res_1 = int(sh.recvline().strip().decode().split(':')[-1])
sh.sendlineafter(b"Enter your number: ",str(level1_m2).encode())
res_2 = int(sh.recvline().strip().decode().split(':')[-1])
sh.recvuntil(b"Now, guess the result of (m | x) + (m | y) for m = ")
guess = int(sh.recvline().strip().decode().split(':')[0])
# starting solve
x = BitVec('x',30)
y = BitVec('y',30)
s = Solver()
s.add((level1_m1 | x) + (level1_m1 | y) == res_1)
s.add((level1_m2 | x) + (level1_m2 | y) == res_2)
if s.check() == sat:
    print(s.model())
    x = s.model().eval(x).py_value()
    y = s.model().eval(y).py_value()
    res = (guess | x) + (guess | y)
    sh.sendline(str(res).encode())

# Level 2
level2_m1 = 0
level2_m2 = int('1'*30,2)
sh.recvuntil(b"Level 2:")
sh.sendlineafter(b"Enter your number: ",str(level1_m1).encode())
res_1 = int(sh.recvline().strip().decode().split(':')[-1])
sh.sendlineafter(b"Enter your number: ",str(level1_m2).encode())
res_2 = int(sh.recvline().strip().decode().split(':')[-1])
sh.recvuntil(b"Now, guess the result of (m | x) + (m ^ y) for m = ")
guess = int(sh.recvline().strip().decode().split(':')[0])

x = BitVec('x',30)
y = BitVec('y',30)
s = Solver()
s.add((level1_m1 | x) + (level1_m1 ^ y) == res_1)
s.add((level1_m2 | x) + (level1_m2 ^ y) == res_2)
if s.check() == sat:
    print(s.model())
    x = s.model().eval(x).py_value()
    y = s.model().eval(y).py_value()
    res = (guess | x) + (guess ^ y)
    sh.sendline(str(res).encode())
    sh.recvuntil(b"Here is your flag:")
    print(sh.recvline().strip().decode())
```



