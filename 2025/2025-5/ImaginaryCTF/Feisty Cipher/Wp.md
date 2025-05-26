分析下加密过程，主要是`helper`这个函数，假设输入的message分块为$A_0,B_0$


$$
A_0,B_0 = A_0,B_0
$$


第一轮`helper()`，用的是key1得到


$$
A_1,B_1= B_0,A_0 \otimes Enc_1(B_0)
$$


第二轮`helper()`，用的是key2得到


$$
A_2,B_2 = B_1, A_1\otimes Enc_2(B_1)
$$


这是经过两轮的加密，解密的话，把两边对换作为输入，并且需要逆着用keys


$$
A_0',B_0' = A_1\otimes Enc_2(B_1),B_1
$$


第一轮`helper()`，此时用的是key2得到


$$
A_1',B_1' = B_1,(A_1\otimes Enc_2(B_1)) \otimes Enc_2(B_1)
$$

$$
A_1',B_1' = B_1,A_1
$$



第二轮`help()`，此时用的是key1得到


$$
A_2',B_2' = A_1,B_1\otimes Enc_1(A_1)
$$


这里$A_1 = B_0,B_1 = A_0\otimes Enc_1(B_0)$，所以最后得到的是


$$
A_2',B_2' = B_0,A_0
$$


本题加密用了100轮这样的操作，原理是一样的，而且`keys`是完全一样的，所以只需要把flag对换即可

```py
# python 3.11.4
from Crypto.Util.number import *
from pwn import *

sh = remote('155.248.210.243',42191)
sh.recvuntil(b'>')
sh.sendline(b'1')
c = int(sh.recvline().strip().decode())
cipher = long_to_bytes(c)
cipher1 = cipher[:16]
cipher2 = cipher[16:]
sh.recvuntil(b'>')
sh.sendline(b'2')
message = bytes_to_long(cipher2 + cipher1)
sh.sendline(str(message).encode())
res = int(sh.recvline().strip().decode().split('>')[-1])
block = long_to_bytes(res)
flag = block[16:] + block[:16]
print(flag)
# ictf{using_1_k3y_1n_f31573l_lol}
```

