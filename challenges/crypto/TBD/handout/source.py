from Crypto.Util.number import getPrime, isPrime, long_to_bytes
from random import randint
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
from flag import flag

def generate_parameters():
    bit_length = 512
    r = getPrime(bit_length)

    while True:
        q = getPrime(bit_length // 12) 
        p = (2 * q * r) + 1
        if isPrime(p):
            break

    while True:
        h = getPrime(bit_length // 12)
        g = pow(h, 2 * r, p)
        if g != 1:
            break

    upper_bound = 10**13 
    a = randint(2, min(p - 2, upper_bound))
    b = randint(2, min(p - 2, upper_bound))

    A, B = pow(g, a, p), pow(g, b, p)
    ss = pow(A, b, p)

    return p,g, A, B,ss


def encrypt(ss, message):
    key = sha256(long_to_bytes(ss)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pad(message, 16)).hex()
    return f"encrypted = {ct}"


p,g,A,B,ss = generate_parameters()
print(f"p: {p}")
print(f"g: {g}")
print(f"A: {A}")
print(f"B: {B}")
print(encrypt(ss, flag))  