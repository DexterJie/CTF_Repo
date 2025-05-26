在模p和模q的有限域下求根，再crt结合

```py
# sage10.6
from Crypto.Util.number import *

p = 182756071972245688517047475576147877841
q = 305364532854935080710443995362714630091
c = 14745090428909283741632702934793176175157287000845660394920203837824364163635
n = 55807222544207698804941555841826949089076269327839468775219849408812970713531

R.<x> = PolynomialRing(Zmod(p))
f = x^4 - c
res1 = f.roots()

R.<x> = PolynomialRing(Zmod(q))
f = x^4 - c
res2 = f.roots()

for mp in res1:
    for mq in res2:
        m = crt([int(mp[0]),int(mq[0])],[p,q])
        print(long_to_bytes(m))
        # NSSCTF{4MM_1s_so_e4s7!}
```

