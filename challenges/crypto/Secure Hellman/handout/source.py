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


    a = randint(2, p-2)
    b = randint(2, p-2)

    A, B = g^a % p, g^b%p
    ss = A^b%p

    return r, q, p, h, g, a, b, A, B, ss

def encrypt(ss, message):
    key = sha256(long_to_bytes(ss)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pad(message, 16)).hex()  
    return f"encrypted = {ct}"

r, q, p, h, g, a, b, A, B, ss = generate_parameters()


print(f"p: {p}")
print(f"g: {g}")
print(f"A: {A}")
print(f"B: {B}")
print(encrypt(ss, flag))