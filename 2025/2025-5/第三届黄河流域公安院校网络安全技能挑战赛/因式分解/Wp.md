# 求hint

爆破vigenere,9秒得到结果

```py
import string

# 定义字符集
dicts = string.ascii_lowercase + "{=}"
dicts_len = len(dicts)

def vigenere_decrypt(cipher, key):
    plaintext = ''
    for i in range(len(cipher)):
        c = cipher[i]
        if c in dicts:
            k = dicts.find(key[i % len(key)])
            idx = (dicts.find(c) - k) % dicts_len
            m = dicts[idx]
            plaintext += m
        else:
            plaintext += c
    return plaintext

import itertools
cipher = "cp=wmaunapgimjfpopeblvup=aywqygb"
for i in itertools.product(dicts,repeat=4):
    tmp = "".join(i)
    key = tmp * 8
    print(f"key = {key},plaintext:{vigenere_decrypt(cipher,key)}")
```

得到

```
key = mlqlmlqlmlqlmlqlmlqlmlqlmlqlmlql,plaintext:tellasecret{a=secert}keepsilentt
```

# 求flag

接着看

```python
assert a**3+b**3+c**3 == 3*a*b*c
gift = secert**3 - 9*secert + 8
print(gift)

assert 3*(p ^ _q) == a + b + c
```

这里可以通过gift的值求出Secret，而根据上面维吉尼亚的明文可以知道`a = secret`

```py
gift = 16174454302590604301534105361719250538317088773024913985896374029052621214070408075926265229111851489902642328975085914458074453963086159246933939207642987161923181946601656883349077418380372857072224674380642689142603970810010050
var('a')
f = a^3 - 9*a + 8 - gift
res = solve([f],[a])
print(res)
```

可以知道

```
a = 25289672915296952421286820568694528489788342353673740247988495109991492893326
```


$$
\because a^3 + b^3 + c^3 = 3abc
$$

移项再因式分解得到
$$
(a+b+c)(a^2 + b^2 + c^2 -ab-bc-ca) = 0
$$
在题目的场景下`a + b + c`不可能是0，那么有
$$
a^2+b^2 +c^2 -ab-bc-ca = 0
$$
所以
$$
a^2 + b^2 + c^2 -ab-bc-ca =
$$

$$
\frac{1}{2}(2a^2 + 2b^2 + 2c^2 -2ab-2bc-2ca)=
$$

$$
\frac{1}{2}((a-b)^2 + (b-c)^2 + (c-a)^2) = 0
$$

显然`a = b = c`，那么`p ^ _q = a`

参考[首尾剪枝](https://tangcuxiaojikuai.xyz/post/342113ee.html)

```py
from Crypto.Util.number import *
import sys
sys.setrecursionlimit(1500)

pxorq = 25289672915296952421286820568694528489788342353673740247988495109991492893326
c = 6470273779347221033316093386019083111753019159457126878637258794718443144439812725263309232245307744208957171971247518708231996986359926490571921925899978
e = 65537
n = 7688109450918412752403544831281002390909833419780604228031807748258766149305710928557842935597759373483911172486806200079137977020089610947423466744079981
pxorq = str(bin(pxorq)[2:]).zfill(256)
 
def find(ph,qh,pl,ql):
    l = len(ph)
    tmp0 = ph + (256-2*l)*"0" + pl
    tmp1 = ph + (256-2*l)*"1" + pl
    tmq0 = qh + (256-2*l)*"0" + ql
    tmq1 = qh + (256-2*l)*"1" + ql
    if(int(tmp0,2)*int(tmq0,2) > n):
        return 
    if(int(tmp1,2)*int(tmq1,2) < n):
        return
    if(int(pl,2)*int(ql,2) % (2**(l-1)) != n % (2**(l-1))):
        return

    if(l == 128):
        pp0 = int(tmp0,2)
        if(n % pp0 == 0):
            print(pp0)
            pf = pp0
            qf = n//pp0
            phi = (pf-1)*(qf-1)
            d = inverse(e,phi)
            m1 = pow(c,d,n)
            print(long_to_bytes(m1))
            exit()

    else:
        if(pxorq[l] == "1" and pxorq[255-l] == "1"):
            find(ph+"1",qh+"0","1"+pl,"0"+ql)
            find(ph+"0",qh+"0","1"+pl,"1"+ql)
            find(ph+"1",qh+"1","0"+pl,"0"+ql)
            find(ph+"0",qh+"1","0"+pl,"1"+ql)
        elif(pxorq[l] == "1" and pxorq[255-l] == "0"):
            find(ph+"1",qh+"0","0"+pl,"0"+ql)
            find(ph+"0",qh+"0","0"+pl,"1"+ql)
            find(ph+"1",qh+"1","1"+pl,"0"+ql)
            find(ph+"0",qh+"1","1"+pl,"1"+ql)
        elif(pxorq[l] == "0" and pxorq[255-l] == "1"):
            find(ph+"0",qh+"0","1"+pl,"0"+ql)
            find(ph+"0",qh+"1","0"+pl,"0"+ql)
            find(ph+"1",qh+"0","1"+pl,"1"+ql)
            find(ph+"1",qh+"1","0"+pl,"1"+ql)
        elif(pxorq[l] == "0" and pxorq[255-l] == "0"):
            find(ph+"0",qh+"0","0"+pl,"0"+ql)
            find(ph+"1",qh+"0","0"+pl,"1"+ql)
            find(ph+"0",qh+"1","1"+pl,"0"+ql)
            find(ph+"1",qh+"1","1"+pl,"1"+ql)

find("1","1","1","1")
```
