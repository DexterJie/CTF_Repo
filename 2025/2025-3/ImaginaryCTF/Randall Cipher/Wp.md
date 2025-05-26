两个字符随便映射为1个字符（保证不重复即可），再注意单独处理单独的`A`，再用quip

```py
import random
import string

c = 'ĀA̰ẢÃ_A̧ẢA̯A̰ÁȂ_ẢÃ_ÀÁȂA̦_ĂÅÄA̱_ÂA̱_ẢÂÃÁA̧ÄȂÁ'
cc = c.replace('_','')
table = string.ascii_uppercase
table = [str(i) for i in table]
table.remove('A')

dic = {}
for i in range(0,len(cc),2):
    tmp = cc[i:i+2]
    if tmp not in dic:
        value = random.choice(table)
        dic[tmp] = value
        table.remove(value)
        
m = ''
for i in range(0,len(cc),2):
    tmp = cc[i:i+2]
    m += dic[tmp]

m = m[:4] + '_' + m[4:10] + '_' + m[10:12] + '_' + m[12:16] + '_' + m[16:20] + '_A' + m[20:22] + '_' + m[22:]
print(m)
# FUMN_WMDUET_MN_QETS_RKJP_AYP_MYNEWJTE
```

quip得到

```
this cipher is very loud and insecure
```

flag为

`ictf{THIS_CIPHER_IS_VERY_LOUD_AND_INSECURE}`