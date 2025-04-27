常规的CBC思路想了一下没出。后来想到可以用randbytes获取一个19968bit的数进行推测。

于是我们假设他第一次返回的是`randbytes(len(msg))`的值，我们传入一个2496bytes的值，pad之后是2512bytes，也就是20096bit。拿这个数据恢复随机数种子，接下来我们都只传入16bytes以内的数据，那么pad之后就是16bytes的值，此时我们预测下一个`randbytes(16)`的值，如果服务器返回的一样，那么我们就能判断此时decision是1，反之是0。这里有两个细节

第一个，randbytes和getrandbits的关系：

```py
    def randbytes(self, n):
        """Generate n random bytes."""
        return self.getrandbits(n * 8).to_bytes(n, 'little')
```

如上，`randbytes(n)`是由`getrandbits(n*8).to_bytes(n,'little')`生成，那么我们用extend_mt19937_predictor提交状态值的时候就需要做一个逆向操作，即

`int.from_bytes(data,'little')`，其中data是我们获取到的2512bytes的值

第二个，需要注意到的是，我们传入16bytes以内的值，服务器会调用一次pad函数，而pad函数定义中又一次调用`random.randbytes(16-len(x)%16)`，

所以我们本地预测的时候要多预测一次，才能和返回的ct对应。

> exp

```py
from extend_mt19937_predictor import ExtendMT19937Predictor
from tqdm import trange
from pwn import *

sh = remote(ip,port)
context.log_level = "critical"

# 假设给的是randbytes(2512)的值
sh.recvuntil(b"msg: ")
send_message = (b"0" * 2496).hex().encode()
sh.sendline(send_message)
sh.recvuntil(b"ct: ")
ct = sh.recvline().strip().decode()
data = bytes.fromhex(ct)
D = int.from_bytes(data,'little')
predictor = ExtendMT19937Predictor()
predictor.setrandbits(D,20096)
sh.sendlineafter(b"[+] ",b"1")

for i in trange(127):
    sh.recvuntil(b"msg: ")
    sh.sendline(b'00')
    n = 16
    predictor.predict_getrandbits(n*8).to_bytes(n,'little')
    tmp = predictor.predict_getrandbits(n*8).to_bytes(n,'little')
    sh.recvuntil(b"ct: ")
    ct = sh.recvline().strip().decode()
    if tmp.hex() == ct:
        sh.sendline(b'1')
    else:
        sh.sendline(b'0')
sh.interactive()
# flag{AES_15_S4f3_3n0ugh_but_MT19937_n07}
```

