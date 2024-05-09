from Crypto.Util.number import getPrime

flag = open('flag.txt', 'rb').read()

assert flag.startswith{b'Spark{'}

p = getPrime(512)
q = getPrime(512)
n = p*q
e = 65537

c = []
for i in flag:
	c.append(pow(i, e, n))

print (f'e = {e}')
print (f'c = {c}')