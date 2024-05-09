def encrypt(ss, message):
    key = sha256(long_to_bytes(ss)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(pad(message, 16)).hex() 
    return f"encrypted = {ct}"