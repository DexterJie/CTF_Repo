https://www.dcode.fr/chiffre-vigenere，已知密钥长度，先用dcode解密一下

```
key1 = BALBAMICVIJUTQR
flag = ictw{is_this_arnd_they_dean_by_ar_ealalanted_oil_arn_isnegai_scheme}
```

有点差错，把key换为`BALSAMICVIJUTQR`，此时得到`ictf{is_this_arnd_they_mean_by_ar_ealalanced_oil_arn_isnegar_scheme}`

`isnegar`正确的应该是`vinegar`，爆破key的倒数二三位

```python
from string import ascii_lowercase

def vigenere_decrypt(cipher, key):
    plaintext = ''
    key = key.lower()
    key_len = len(key)
    idx = 0
    for c in cipher:
        if c in ascii_lowercase:
            k = ord(key[idx % key_len]) - ord('a')
            p = (ord(c) - ord('a') - k) % 26
            plaintext += chr(p + ord('a'))
            idx += 1
        else:
            plaintext += c
    return plaintext

cipher = "jcex{ie_bjda_jlgt_kiej_eemv_dt_ia_ytbrmayuep_wkg_iah_biefglj_sopghm}"
key = 'BALSAMICVIJUTQR'.lower()

import itertools
for i in itertools.product(ascii_lowercase,repeat=2):
    tmp = ''.join(i)
    key = 'balsamicviju' + tmp + 'r'
    m = vigenere_decrypt(cipher, key)
    if 'vinegar' in m:
        print(f"key = {key} : plaintext: {m}")
```

此时得到

```
key = balsamicvijugar : plaintext: ictf{is_this_arat_they_mean_by_ar_enbalanced_oil_arn_vinegar_scheme}
```

猜测`arn`就应该是`and`

```py
from string import ascii_lowercase

def vigenere_decrypt(cipher, key):
    plaintext = ''
    key = key.lower()
    key_len = len(key)
    idx = 0
    for c in cipher:
        if c in ascii_lowercase:
            k = ord(key[idx % key_len]) - ord('a')
            p = (ord(c) - ord('a') - k) % 26
            plaintext += chr(p + ord('a'))
            idx += 1
        else:
            plaintext += c
    return plaintext

cipher = "jcex{ie_bjda_jlgt_kiej_eemv_dt_ia_ytbrmayuep_wkg_iah_biefglj_sopghm}"
key = 'BALSAMICVIJUTQR'.lower()

import string
import itertools
for i in itertools.product(string.ascii_lowercase,repeat=2):
    tmp = ''.join(i)
    key = 'balsamicvi' + tmp + 'gar'
    m = vigenere_decrypt(cipher, key)
    if 'and' in m:
        print(f"key = {key} : plaintext: {m}")
```

此时得到

```
key = balsamicvinegar : plaintext: ictf{is_this_what_they_mean_by_an_unbalanced_oil_and_vinegar_scheme}
```

