from Crypto.Util.number import*
import random
import string
from secret import flag,key

def shash(value,key):
    assert type(value) == str
    assert type(key) == int
    length = len(value)

    if length == 0:
        return 0
    mask = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    x = (ord(value[0]) << 7) & mask
    for c in value:
        x = (key * x) & mask ^ ord(c)

    x ^= length & mask

    return x

def get_test(key):

    testvalue = []
    testhash = []

    for i in range(64):
        a = ''.join(random.choices(string.ascii_letters + string.digits, k=32)) 
        testvalue.append(a)
        testhash.append(shash(a,key))

    return testvalue,testhash

if __name__ == "__main__":
    assert len(flag) == 32
    assert type(flag) == str
    key = getRandomInteger(128)
    testvalue,testhash = get_test(key)
    shash = shash(flag,key)
    with open('output.txt', 'a') as f:
        f.write('testvalue = ' + str(testvalue) + '\n')
        f.write('testhash = ' + str(testhash) + '\n')
        f.write('shash = ' + str(shash) + '\n')    