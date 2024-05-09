from Crypto.Util.number import *

flag = open("flag.txt","rb").read()
flag = bytes_to_long(flag)
e = 65537
p = getPrime(512)
n = p*p*p
c = pow(flag, e, n)

print (f"n = {n}")
print (f"c = {c}")