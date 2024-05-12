from Crypto.Util.number import getPrime, bytes_to_long, inverse
from random import getrandbits
from math import gcd
from SECRET import flag

m = bytes_to_long(flag)

def safe_rsa():
    p = getPrime(1024)
    q = getPrime(1024)
    N = p*q
    phi = (p-1)*(q-1)
    while True:
        d = getrandbits(512)
        if gcd(d,phi) == 1:
            e = inverse(d, phi)
            break
    return N,e,d


N,e = safe_rsa()
c = pow(m, e, N)

print(f'N = {hex(N)}')
print(f'e = {hex(e)}')
print(f'c = {hex(c)}')
