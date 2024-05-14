from pwn import remote, log
import json
from randcrack import RandCrack

rc = RandCrack()

io = remote('4.232.65.83', 5000)

rcv = io.recvuntil(b"> Gimme a number: ").decode()

print(rcv)

print("-----------------------------------")

received = rcv.split('\n')[0]

received = received.replace("'", '"')

tofeed = json.loads(received)

for i in tofeed['given']:
    rc.submit(i)

while True:
    guess = rc.predict_randrange(0, 4294487295)
    print(guess)
    io.sendline(str(guess))
    r = io.clean()
    print(r)
