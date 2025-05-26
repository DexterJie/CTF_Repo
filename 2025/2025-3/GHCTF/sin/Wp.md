$$
c = 2sin(m) - 2sin(m)\times cos(2m)
$$



化简得到


$$
c = 4sin^3(m)
$$


即


$$
\therefore sin(m) = \sqrt[3]{\frac{c}{4}}
$$



把等号右边这个记为tmp


$$
\therefore m = arcsin(tmp) + 2k\pi
$$



这个时候构造格


$$
\begin{pmatrix}
m & 1 & k
\end{pmatrix}
\begin{pmatrix}
1 & 0 & 1\\
0 & 256^k & arcsin(tmp)\\
0 & 0 & 2\pi
\end{pmatrix} = \begin{pmatrix}
m & 256^k & 0
\end{pmatrix}
$$


这个格显然是不够准确的，因为我们不知道flag的长度，所以钥通过爆破的方式来配平中间这个1。

```py
# sage10.6
from Crypto.Util.number import long_to_bytes,bytes_to_long
import math

c = 0.002127416739298073705574696200593072466561264659902471755875472082922378713642526659977748539883974700909790177123989603377522367935117269828845667662846262538383970611125421928502514023071134249606638896732927126986577684281168953404180429353050907281796771238578083386883803332963268109308622153680934466412
cc = (c / 4)**(1/3)
precision = 1024
T = 2**precision

for length in range(30,70):
    M = Matrix(QQ,[
        [1,0,1],
        [0,256^length,arcsin(cc)],
        [0,0,2*pi.n(precision)]
    ])
    M[:,-1] *= T
    for line in M.LLL():
        m = abs(line[0])
        flag = long_to_bytes(int(m))
        if b'NSSCTF' in flag:
            print(flag)
            break
            # NSSCTF{just_make_a_latter_and_LLL_is_OK_padpad}
```

另外一种方法思路如下：


$$
\therefore m = arcsin(tmp) + 2k\pi
$$


在这个式子中，我们知道了flag的头和尾，可以把上式写为


$$
m_1 + known = arcsin(tmp) + 2k\pi
$$


这个`known = bytes_to_long(b'NSSCTF{' + b'\x00'*length + b'}')`

这个情况下可以把目标值变小，提高规约成功率


$$
\begin{pmatrix}
m_1 & 1 & k
\end{pmatrix}
\begin{pmatrix}
1 & 0 & 1\\
0 & 1 & arcsin(tmp) - known\\
0 & 0 & 2\pi
\end{pmatrix} = \begin{pmatrix}
m_1 & 1 & 0
\end{pmatrix}
$$



```py
# sage10.6
from Crypto.Util.number import long_to_bytes,bytes_to_long
import math

c = 0.002127416739298073705574696200593072466561264659902471755875472082922378713642526659977748539883974700909790177123989603377522367935117269828845667662846262538383970611125421928502514023071134249606638896732927126986577684281168953404180429353050907281796771238578083386883803332963268109308622153680934466412
cc = (c / 4)**(1/3)
precision = 1024

for length in range(30,70):
    tmp = bytes_to_long(b'NSSCTF{' + b'\x00'*length + b'}')
    approx_m = arcsin(cc)
    
    T = 2**precision
    M = Matrix(QQ,[
        [approx_m - tmp,0,0],
        [pi.n(precision),1,0],
        [1,0,1]
    ])
    M[:,0] *= T
    for line in M.LLL():
        m = int(abs(line[-1])) + tmp
        flag = long_to_bytes(m)
        if b'NSSCTF' in flag:
            print(flag)
```
