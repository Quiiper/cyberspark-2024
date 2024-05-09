from Crypto.Util.number import bytes_long, getPrime

flag = open('flag.txt', 'rb').read()
flag = bytes_to_long(flag)

assert len(bin(flag)) == 241

e = 3
p = getPrime(357)
q = getPrime(357)
n = p*q
c = pow(flag, e, n)

print (f"c = {c}")
print (f"n = {n}")