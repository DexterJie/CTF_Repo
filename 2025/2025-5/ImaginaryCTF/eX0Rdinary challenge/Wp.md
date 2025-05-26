先base64解码，然后尝试异或ictf{，得到}ictf。

所以加密逻辑为`c[i] = m[i] ^ m[i-1]`

```py
import base64

c = "FAoXEh0PHAEaLDYaLD4+LwIXEQANJiwHERcXChsNCRUBOycXHS08CwkNADM9FwErPg8XDhYYCiw4CAALOzUFDT03CRcTOj4+OQoNBho="
c = base64.b64decode(c)

flag = b'i'
for i in range(1,len(c)):
    flag += chr(c[i] ^ flag[i-1]).encode()

print(flag)
# ictf{this_is_a_pretty_stereotyped_xor_chall_but_anyways_good_job_have_a_flag}
```

