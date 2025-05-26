对于b的每个bit有


$$
b_i = A_{0,i} \otimes A_{1,i} \otimes ...\otimes A_{47,i}
$$


也就是


$$
b_i = A_{0,i} + A_{1,i} + ...+ A_{47,i} \mod 2
$$


可以用矩阵表示


$$
\begin{pmatrix}
a_0 & a_1 & ... & a_{48}
\end{pmatrix}
\begin{pmatrix}
A_{0,0} & A_{0,1} & ... & A_{0,63}\\
A_{1,0} & A_{1,1} & ... & A_{1,63}\\
\vdots & \vdots & \ddots & \vdots\\
A_{47,0} & A_{47,1} & ... & A_{47,63}
\end{pmatrix} = \begin{pmatrix}
b_0 & b_1 & ... & b_{63}
\end{pmatrix}
$$


解矩阵方程得到左边的a向量即可

```py
# sage10.6
from Crypto.Cipher import AES
from hashlib import sha256
from pwn import *

sh = remote("155.248.210.243",42121)
datas = eval(sh.recvline().strip().decode())
A = datas['A']
b = datas['b']
c = datas['c']

cipher = bytes.fromhex(c.split(';')[0])
iv = bytes.fromhex(c.split(';')[1])
A_matrix = Matrix(GF(2),[[int(i) for i in bin(a)[2:].zfill(64)] for a in A])
b_vector = vector(GF(2),[int(i) for i in bin(b)[2:].zfill(64)])
print(A_matrix.dimensions())
a_vector = A_matrix.solve_left(b_vector)
a = int(''.join(list(map(str,a_vector))[::-1]),2)

key = sha256(str(a).encode()).digest()
aes = AES.new(key, AES.MODE_CBC, IV=iv)
flag = aes.decrypt(cipher)
print(flag)
# ictf{XOR_m337_in_th3_m1ddl3}
```

