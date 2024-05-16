import os
import sys
from pwn import *
from Crypto.Util.number import *
path = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
if sys.path[1] != path:
    sys.path.insert(1, path) 
r = process(["python3", "server.py"])
r.recv()
r.sendline(b'2')
secret=r.recvuntil(b"}").split(b':')[1].split(b'}')[0].decode().strip()
sig = secret.replace("'","")

r.recv()
r.sendline(b'3')
r.recv()
r.sendline(sig.encode())
response = r.recv().split(b':')[1].split(b'}')[0].decode().strip()
m = response.replace("'","")
m= m[2:]
flag= int(m, 16)
print(long_to_bytes(flag))
'''
Pretty basic task it's obvious when choosing the second option we'll get that the secret is getting encrypted with the values of the public key. And choosing the 3rd option the server will take ur input put it to the power of d mod n ( decryption in rsa ) so that's it we will get our signature then just decrypt it throught the server. I made a small pwn tools script sadly the remote access for this task is down but you can try it out locally as you have all the files needed in this repo
Hopefully you enjoyed the crypto tasks in this ctf Cy@ next time 
'''

#flag : Spark{Th3_W04St_S1gn1ng_C0mp4nY_3v3r}
#Author : Quiiper
