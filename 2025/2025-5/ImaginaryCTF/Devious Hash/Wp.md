`p = 2**521 - 1`,那`&p`相当于`% 2**521`，第一轮的结果是


$$
hash = A^2 \mod p
$$


第二轮的时候则是


$$
hash = (A^2 +A \mod (p+1))^2 \mod p
$$


`mod (p+1)`可以写为`- (p+1)`，其实每一轮的这一步要么`- (p+1)`要么不减，所以可以爆破出这个多项式

> exp

```python
from Crypto.Util.number import *
import itertools

p = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
mod = p + 1
c = 5529146955026504451007428379478468505767752969729288045439800587429289159437142456530335848325725612485348038928038452092595039114633083434109252927938183950

R.<A> = PolynomialRing(Zmod(p))
# 第一轮结束后的f
for i in itertools.product([0,1],repeat=7):
    f = A^2
    print(i)
    for _ in i:
        f += A
        f -= _ * mod
        f = f ^ 2
    f -= c
    try:
        res = f.monic().roots()
        for root in res:
            m = long_to_bytes(int(root[0]))
            if b'ictf' in m:
                print(m)
                break
    except:
        pass
    # ictf{devious_mersenne_prime_makes_root_finding_easy_actually}
```

