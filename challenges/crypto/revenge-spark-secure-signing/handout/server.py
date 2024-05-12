import random
from Crypto.Util.number import bytes_to_long, getPrime
from SECRET import flag

welcome = """
Experience Spark Security’s Signature Service. This time you won’t be able to leak anything"""

def option():
    print("1 - get signature")
    print("2 - leave")

def initialize_challenge():
    p = getPrime(1024)
    q = getPrime(1024)
    N = p * q
    e = 11
    return p, q, N, e

def main(welcome):
    print(welcome)
    p, q, N, e = initialize_challenge()
    while True:
        option()
        your_input = str(input("Choose an option: "))
        response = challenge(your_input, N, e)
        print(response)
        if your_input == '2':
            break

def pad(flag, N):
    m = bytes_to_long(flag)
    a = random.randint(2, N)
    b = random.randint(2, N)
    return (a, b), a*m+b

def encrypt(flag, N, e):
    pad_var, pad_msg = pad(flag, N)
    encrypted = (pow(pad_msg, e, N), N)
    return pad_var, encrypted

def challenge(your_input, N, e):
    if your_input == '1':
        pad_var, encrypted = encrypt(flag, N, e)
        return {"encrypted_flag": encrypted[0], "modulus": encrypted[1], "padding": pad_var}

    elif your_input == '2':
        return "Goodbye!"

    else:
        return "Invalid option, try again"
    
if __name__ == "__main__":
    main(welcome)