#!/usr/local/bin/python

import random, time

x = random.randint(80, 120)

ll = [random.randrange(0,4294967294) for _ in range(624)]

togive = {"given":ll}

print(togive)
for i in range(x):
    try:
        inpp = input('> Gimme a number: ')
        if(len(inpp) > 11):
            print('What are you trying to do? Bye!')
            exit(0)
        inp = int(inpp)
    except:
        print('Wrong! try again')
        print('Exiting...')
        exit(0)
    ran = random.randrange(0, 4294487295)
    if inp == ran:
        print('Correct! continue')
    else:
        print('Wrong! try again')
        print('Exiting...')
        exit(0)

print('Here is your flag: Spark{fake_flag}')
exit(0)