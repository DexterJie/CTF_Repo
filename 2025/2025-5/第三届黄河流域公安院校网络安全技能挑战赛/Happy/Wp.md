`fuc0`中生成bit的逻辑等价于

$$
bit = \begin{pmatrix}
s_0 & ... & s_{127}
\end{pmatrix}
\begin{pmatrix}
m_0\\
\vdots \\
m_{127}
\end{pmatrix}
\mod 2
$$

那么newstate和state的线性关系如下，前127行表示左移，最后一行表示newbit的生成


$$
\begin{pmatrix}
s_{i+1} \\ s_{i+2} \\ \vdots \\ s_{i+128}
\end{pmatrix} = \begin{pmatrix}
0 & 1 & ... & 0\\
0 & 0 & ... & 0\\
\vdots & \vdots & \ddots & \vdots\\
m_0 & m_1 & ... & m_{127} 
\end{pmatrix}
\times 
\begin{pmatrix}
s_i \\ s_{i+1} \\ \vdots \\ s_{i+127}
\end{pmatrix}
$$

```py
mask = 109908700282042807039366676242995409413
mask_vec = vector(GF(2),list(map(int,bin(mask)[2:].zfill(128))))
L = [[0 for _ in range(128)]for i in range(127)]
for i in range(127):
    L[i][i+1] = 1
L = Matrix(GF(2),L)
L = L.stack(mask_vec)
```

以`seed = 108217052284215322438501043708351357094`，`newstate = 216434104568430644877002087416702714188`为例进行验证

```python
mask = 109908700282042807039366676242995409413
mask_vec = vector(GF(2),list(map(int,bin(mask)[2:].zfill(128))))
seed = 108217052284215322438501043708351357094
seed_vec = vector(GF(2),list(map(int,bin(seed)[2:].zfill(128))))
new = int(''.join(map(str,L * seed_vec)),2)
print(new)
# 216434104568430644877002087416702714188
```

根据msg的已知部分，还有flag头，我们能获得前16个字节和最后1个字节。这里每个字节的bit是2023次seed迭代产生的

这里看第一个字节，记为`out1`，它的第一个bit记为`bit1`，`bit1 = s2023`

$$
\begin{pmatrix}
s_{1876} \\ s_{1877} \\ \vdots \\ s_{2023}
\end{pmatrix} = \begin{pmatrix}
0 & 1 & ... & 0\\
0 & 0 & ... & 0\\
\vdots & \vdots & \ddots & \vdots\\
m_0 & m_1 & ... & m_{127} 
\end{pmatrix}^{2023}
\times 
\begin{pmatrix}
s_{0} \\ s_{1} \\ \vdots \\ s_{127}
\end{pmatrix}
$$

记 $M = L^{2023}$ ,那么 $s_{2023}$ 可以通过M最后一行乘上seed得到，即`bit1 = M[-1] * seed_vec`

第二个bit是 $s_{4046}$ ，同理`bit2 = M^2[-1] * seed_vec`

aaaa

$$
\begin{pmatrix}
out_{1,1}\\
out_{1,2}\\
out_{1,3}\\
out_{1,4}\\
out_{1,5}\\
out_{1,6}\\
out_{1,7}\\
out_{1,8}
\end{pmatrix}
_{8\times 1} = \begin{pmatrix}
M_1\\
M_2\\
M_3\\
M_4\\
M_5\\
M_6\\
M_7\\
M_8
\end{pmatrix}
_{8\times 128}
\times
\begin{pmatrix}
s_{0} \\ s_{1} \\ \vdots \\ s_{127}
\end{pmatrix}_{128\times 1}
$$

记第二个字节为`out2`，它与seed存在下面的关系

$$
\begin{pmatrix}
out_{2,1}\\
out_{2,2}\\
out_{2,3}\\
out_{2,4}\\
out_{2,5}\\
out_{2,6}\\
out_{2,7}\\
out_{2,8}
\end{pmatrix}
_{8\times 1} = \begin{pmatrix}
M_9\\
M_{10}\\
M_{11}\\
M_{12}\\
M_{13}\\
M_{14}\\
M_{15}\\
M_{16}
\end{pmatrix}
_{8\times 128}
\times
\begin{pmatrix}
s_{0} \\ s_{1} \\ \vdots \\ s_{127}
\end{pmatrix}_{128\times 1}
$$

每个out可以与seed建立8个方程，用上前16个字节，建立下面的矩阵方程即可解出seed

$$
\begin{pmatrix}
out_{1,1}\\
out_{1,2}\\
\vdots \\
out_{60,8}\\
\end{pmatrix} = \begin{pmatrix}
M_1\\
M_2\\
\vdots \\
M_{480}
\end{pmatrix}
\times\begin{pmatrix}
s_{0} \\ s_{1} \\ \vdots \\ s_{127}
\end{pmatrix}
$$

解出seed后带回就可以求flag了

> 求seed

```py
# sage10.6
from Crypto.Util.strxor import strxor as xor
from Crypto.Util.number import *

mask = 109908700282042807039366676242995409413
mask_vec = vector(GF(2),list(map(int,bin(mask)[2:].zfill(128))))
c = "cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48"
enc = bytes.fromhex(c)
knwon = bytes_to_long(xor(b'Happy4321: flag{',enc[:16]))
knwon_vec = vector(GF(2),list(map(int,bin(knwon)[2:].zfill(128))))

# 状态变化矩阵L
L = [[0 for _ in range(128)]for i in range(127)]
for i in range(127):
    L[i][i+1] = 1
L = Matrix(GF(2),L)
L = L.stack(mask_vec)
# M矩阵
M = L^2023
A = Matrix(GF(2),128,128)

for i in range(128):
    A[i] = (M^(i+1))[-1]

seed_vec = A.solve_right(knwon_vec)
print(seed_vec)
# (0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0)
```

> 求flag

```py
# python
class Gen:
    def __init__(self, state):
        self.nbits = 128
        self.state = state & ((1 << self.nbits) - 1)
        self.mask = 109908700282042807039366676242995409413


    def func0(self, steps=1):
        for _ in range(steps):
            res = self.state & self.mask
            bit = sum([(res >> i) & 1 for i in range(self.nbits)]) & 1
            self.state = ((self.state << 1) ^ bit) & ((1 << self.nbits) - 1)
        return bit

    def __next__(self):
        out = 0
        for _ in range(8):
            bit = self.func0(2023)
            out = (out << 1) ^ bit
        return out

c = "cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48"
enc = bytes.fromhex(c)
seed_vec = (0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0)
seed = int(''.join(map(str, seed_vec)), 2)
print(seed)
gen = Gen(seed)
flag = bytes(c ^ next(gen) for c in enc)
print(flag)
# Happy4321: flag{The_matrix_is_as_charming_as_the_starry_sky}
```



