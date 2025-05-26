参考:[Maple3412'Blog](https://blog.maple3142.net/2021/04/08/angstromctf-2021-writeups/#thunderbolt)

```py
S[i] ^= S[j]
S[j] ^= S[i]
S[i] ^= S[j]
```

这种交换只在`S[i] != S[j]`的情况下有效，如果`S[i] == S[j]`会把两个都设置成0，而RC4在swap的时候本来就有可能遇到两个相同的值交换的情形，当key的长度越高，概率越大，在这种情况下很有可能让密钥流置为0，所以最后的密文就是flag本身。

受此启发，让key的长度越长越好

> exp.py

```py
from pwn import *

# context.log_level = 'debug'
sh = remote('155.248.210.243',42138)
sh.sendline(b'1'*300000)
print(sh.recvline().strip().decode())

# ictf{why_us1ng_tr1pIe_x0r_1n_Crypt0syst3m}
```

