#!/usr/local/bin/python

from SECRET import n,e,d,secret
from Crypto.Util.number import *
welcome = """
Experience Spark Security’s Signature Service. Trust in Spark Security—where messages are sealed tight.
"""


def option():
    print("1 - get public key")
    print("2 - Get secret message")
    print("3 - sign")
    print("4 - leave")

def main():
    print(welcome)
    result = None

    while True:
        try:
            option()
            choice = int(input("> "))
        except:
            print("Try again.")
            continue

        if choice == 1:
            result = {"N": hex(n), "e": hex(e) }
        elif choice == 2:
            m = bytes_to_long(secret)
            result = {"secret": hex(pow(m, e, n)) }
        elif choice == 3:
            print("Enter message to sign: ")
            msg = int(input("> "), 16)
            result = {"signature": hex(pow(msg, d, n)) }
        else:
            print("Cy@")
            exit(0)

        print(result)

if __name__ == "__main__":
    main()