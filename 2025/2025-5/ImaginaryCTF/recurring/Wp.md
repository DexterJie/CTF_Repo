
$$
t_1 = m_1\times 2^{m_1} \mod p
$$




$$
t_2 = m_2\times 2^{m_2} \mod p
$$




$$
t_3 = (m_2-m_1)\times 2^{m_2-m_1} \mod p
$$




$$
t_4 = (m_2 + m_1)\times 2^{m_2+m_1} \mod p
$$



做一些化简


$$
t_3t_4t_2^{-2} = (m_2^2 - m_1^2)2^{2m_2}\times m_2^{-2}2^{-2m_2} \mod p = 1-(\frac{m_1}{m_2})^2 \mod p
$$




$$
t_4t_3^{-1}t_1^{-2} = (m_2+m_1)(m_2-m_1)^{-1}2^{2m_1} \times m_1^22^{-2m_1} \mod p =  \frac{m_2+m_1}{m_1^2(m_2-m_1)} \mod p
$$



用结式消去未知数然后求解

> exp

```py
# sage10.6
# 定义有限域
p = 0xafe4dfec75d05b8204f949749dce9d69eaee982528f7e2c177862b4f12b635d9
# 参数定义
t1 = 0x6d04f0ebde78ca72c0a65629cd6f2cc337319c05b266ed789843ea2bdf11551f
t2 = 0x61483d050ad72a0e6dda11e3f683fbac20ab17b4a26615ac3eb4fbaecef519bd
t3 = 0x13c9395628b7f90ff1675d73cc97ae24ea5c9993366364627d20f9f52b19fabb
t4 = 0x75e04f3f38420029fa57934de57b6fb59f9615e4be32eaa4460c57a47c2842ae

a = t3 * t4 * pow(t2,-2,p) % p
b = t4 * pow(t3,-1,p) * pow(t1,-2,p) % p

R.<m1, m2> = PolynomialRing(Zmod(p))
f = a * m2^2 + m1^2 - m2^2
g = b * (m2 - m1)*m1^2 - (m2 + m1)
# 消去m2
h1 = f.sylvester_matrix(g,m2).det()
PR.<m1> = PolynomialRing(Zmod(p))
h1 = PR(h1)
roots = h1.roots()
for root in roots:
    print(long_to_bytes(int(root[0])))

# 消去m1
h2 = f.sylvester_matrix(g,m1).det()
PR.<m2> = PolynomialRing(Zmod(p))
h2 = PR(h2)
roots = h2.roots()
for root in roots:
    print(long_to_bytes(int(root[0])))
# ictf{wh4t_ev3n_i5_@_r34l_w0r1d_4ppl1c4ti0n_9OoYVHHxYhQG6teVZXHC}
```

