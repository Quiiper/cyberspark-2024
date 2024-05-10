from Crypto.Util.number import bytes_to_long,getPrime

flag = open('flag.txt', 'rb').read()

p = getPrime(512)
q = getPrime(512)
n = p*q
phi = (p-1)*(q-1)

e = 65537
e1 = pow(e,e)
e2 = pow(e,e1)

c = pow(bytes_to_long(flag), e2, n)

print(f"n = {n}")
print(f"c = {c}")
print(f"phi = {phi})
