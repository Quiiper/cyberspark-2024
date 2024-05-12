from Crypto.Util.number import getPrime, bytes_to_long

flag = open("flag.txt","rb").read()
flag = bytes_to_long(flag)
p = getPrime(128)
q = getPrime(128)
n = p*q
e = getPrime(7)

c = []
for i in flag:
	c.append(pow(i, e, n))

print (f"n = {n}")
print (f"c = {c}")