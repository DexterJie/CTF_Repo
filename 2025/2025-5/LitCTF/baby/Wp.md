由题意知


$$
data \equiv tm^{-1} \mod g
$$


所以


$$
data\times m \equiv t \mod g
$$


即


$$
t = data\times m -kg
$$


造格


$$
\begin{pmatrix}
m & k
\end{pmatrix}
\begin{pmatrix}
1 & c \\
0 & g
\end{pmatrix} = \begin{pmatrix}
m & t
\end{pmatrix}
$$


做一点参数调整即可

```py
# sage10.6
from Crypto.Util.number import *

g = 7835965640896798834809247993719156202474265737048568647376673642017466116106914666363462292416077666356578469725971587858259708356557157689066968453881547
data = 2966297990428234518470018601566644093790837230283136733660201036837070852272380968379055636436886428180671888655884680666354402224746495312632530221228498
i = 128
Ge = Matrix(ZZ,[
    [1,data],
    [0,g]
])
Ge[:,-1] *= 2^i
m,t = Ge.LLL()[0]
m,t = abs(m),abs(t) // 2^i
if t.bit_length() == 150:
    print(long_to_bytes(m))
# LitCTF{56008a819331c9f3608a718327b7e6ce}
```

