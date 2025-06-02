迷迷糊糊的一题。我太菜了😭

`H4sh`的计算可以看作一个关于 $a$ 的小系数多项式


$$
res = 128c_0a^{32} + x_0a^{31} + x_1a^{30} + ... + x_{30}a + x_{31} \mod p
$$


这里`a = key`，对每个hash来说

用矩阵表达就是


$$
\begin{pmatrix}
128a^{32} & a^{31} & ... & 1
\end{pmatrix}\_{1\times 33}
\begin{pmatrix}
c_{1,0} & c_{2,0} & ... & c_{m,0}\\
x_{1,0} & x_{2,0} & ... & x_{m,0}\\ 
\vdots & \vdots & \ddots & \vdots \\
x_{1,31} & x_{2,31} & ... & x_{m,31}
\end{pmatrix}\_{33 \times m} = \begin{pmatrix}
h_1 & h_2 & ... & h_m
\end{pmatrix}\_{1\times m}
$$


记 $a_i$ 为左边这个向量中的元素， $\vec{x_i}$ 为矩阵中的行向量。于是也可以把式子记为


$$
\vec{h} = a_1\vec{x_1} + ... + a_n\vec{x_n} \mod p
$$


造格


$$
\begin{pmatrix}
u_1 & u_2 & ... & u_{65} & k
\end{pmatrix}\_{1\times 66}
\begin{pmatrix}
Kh_1 & 1 & 0 & ... & 0\\
Kh_2 & 0 & 1 & ... & 0\\
\vdots & \vdots & \vdots & \ddots & \vdots\\
Kh_{65} & 0 & 0 & ... & 0\\
Kp & 0 & 0 & ... & 0
\end{pmatrix}\_{66 \times 66} = \begin{pmatrix}
\sum_{i=1}^{65}u_ih_i \mod p & u_1 & u_2 & ... & u_{65}
\end{pmatrix}\_{1\times 66}
$$


这些分析是我瞎掰的。可以直接跳到思路那里

如果 $\sum_{i=1}^{65}u_ih_i = 0\mod p \longrightarrow \vec{u} \cdot \vec{h} = 0 \mod p $


$$
\left \langle \vec{u},\vec{h} \right \rangle = a_1\left \langle \vec{u},\vec{x_1} \right \rangle + ... + a_n\left \langle \vec{u},\vec{x_n} \right \rangle \equiv 0 \mod p
$$


令向量 $\vec{P_u} = (\left \langle \vec{u},\vec{x_1} \right \rangle \quad ... \quad \left \langle \vec{u},\vec{x_n} \right \rangle )$

这就意味着 $\vec{P_u}$ 与向量 $\vec{a} = (a_1 \quad a_2 \quad ... \quad a_n)$ 在模 $p$ 下垂直。我们寻找足够短的向量 $\vec{u}$ ，由于 $x_i$ 中的元素介于 $[-256,256]$ ，这导致 $\vec{P_u}$ 也很短。

在模 $p$ 下，与 $\vec{a}$ 正交的核空间中，存在最短的向量，记它的模长为 $\gamma$ ，此时如果 $\vec{u}$ 的模长远远小于 $\gamma$ ，从而 $\left \langle \vec{u},\vec{x_i} \right \rangle$ 也远小于 $\gamma$ ，即 $\vec{P_u}$ 的模长小于 $\gamma$ 并且和 $\vec{a}$ 正交，就只能满足 $\vec{P_u}=0$ ，因此我们得到的 $\vec{u}$ 会在整数环上正交所有 $\vec{x_i}$ 。



那思路就是，找出足够多正交于 $\vec{h}$ 的足够短的向量 $\vec{u_i}$ ，再对 $\vec{u_i}$ 构成的矩阵LLL规约得到 $\vec{x_i}$ 向量，再求解矩阵方程得到 $\vec{a}$

```py
from Crypto.Util.number import getPrime
from pwn import *
import random
context.log_level = 'error'  # 只显示错误信息，不显示连接日志

class FNV():
    def __init__(self):
        self.pbit = 1024
        self.p = getPrime(self.pbit)
        self.key = random.randint(0, self.p)
    
    def H4sh(self, value:str):
        length = len(value)
        x = (ord(value[0]) << 7) % self.p
        for c in value:
            x = ((self.key * x) % self.p) ^^ ord(c)
        x ^^= length
        return x

while True:
    sh = remote('127.0.0.1',10007)
    # get p
    sh.recvuntil(b"option >")
    sh.sendline(b'G')
    p = int(sh.recvline().decode().strip().split('=')[-1])
    # get h
    n = 65
    h = []
    for i in range(n):
        sh.recvuntil(b"option >")
        sh.sendline(b'H')
        hi = int(sh.recvline().decode().strip().split(':')[-1])
        h.append(hi ^^ 32)
    # 用h_i造格，找短向量
    Ge = Matrix(ZZ,n+1,n+1)
    for i in range(n):
        Ge[i,0] = h[i]
        Ge[i,i+1] = 1
    Ge[-1,0] = p
    Ge[:,0] *= getPrime(1024)
    # for line in flatter(Ge):
    #     print(line)
    #     print(int(line.norm()))
    # 找出32组满足条件的向量
    u_matrix = Ge.LLL()[:32,1:]
    u_right_kernel = u_matrix.right_kernel(algorithm = 'pari').matrix()     # 33 * 65
    X = u_right_kernel.LLL()
    # 通过aX = h求解a
    vec_h = vector(GF(p),h)
    a = X.change_ring(GF(p)).solve_left(vec_h)
    a = list(map(int,a.list()))
    # key在a中,但是不知道具体的位置,只能爆
    key = a[-2]
    fnv = FNV()
    fnv.p = p
    fnv.key = key
    sh.recvuntil(b"option >")
    sh.sendline(b'F')
    c = sh.recvline().strip().decode().split(':')[-1].strip()
    h = fnv.H4sh(c)
    sh.sendlineafter(b"Could you tell the value of H4sh(x)?",str(h).encode())
    res = sh.recvline().strip().decode()
    if "Congratulations!" in res:
        flag = sh.recvline().strip().decode()
        print(flag)
        break
    sh.close()
```





