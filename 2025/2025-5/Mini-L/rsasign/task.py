from Crypto.Util.number import bytes_to_long, getPrime, inverse
from secret import flag


def genKeys(nbits):
    e = 0x10001
    p = getPrime(nbits // 2)
    q = getPrime(nbits // 2)
    n = p * q
    phi = n - (p + q) + 1
    d = inverse(e, phi)
    pubkey = (n, e)
    prikey = (d, p, q)
    
    return pubkey, prikey


def encrypt(msg, pubkey):
    m = bytes_to_long(msg)
    n, e = pubkey
    c = pow(m, e, n)
    return c


def get_gift(prikey):
    a = bytes_to_long(b'miniL')
    b = bytes_to_long(b'mini7')
    p, q = prikey[1:]
    phi = (p - 1)*(q - 1)
    giftp = p + a
    giftq = q + b
    gift = pow((giftp + giftq + a*b), 2, phi)
    return gift >> 740


if __name__ == "__main__":
    nbits = 1024
    pubkey, prikey = genKeys(nbits)
    c = encrypt(flag, pubkey)
    gift = get_gift(prikey)
    with open('output.txt', 'a') as f:
        f.write('pubkey = ' + str(pubkey) + '\n')
        f.write('c = ' + str(c) + '\n')
        f.write('gift = ' + str(gift) + '\n')
        
"""
pubkey = (65537,103894244981844985537754880154957043605938484102562158690722531081787219519424572416881754672377601851964416424759136080204870893054485062449999897173374210892603308440838199225926262799093152616430249061743215665167990978654674200171059005559869946978592535720766431524243942662028069102576083861914106412399)
c = 50810871938251627005285090837280618434273429940089654925377752488011128518767341675465435906094867261596016363149398900195250354993172711611856393548098646094748785774924511077105061611095328649875874203921275281780733446616807977350320544877201182003521199057295967111877565671671198186635360508565083698058
gift = 2391232579794490071131297275577300947901582900418236846514147804369797358429972790212
"""