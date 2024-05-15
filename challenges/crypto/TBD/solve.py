'''
The idea here is pretty basic we just need to calculate "a" with the discrete_log and after that we can just get the shared secret by calculating (B**a % p) 
'''

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes, inverse
from hashlib import sha256
from sympy.ntheory import discrete_log
p= 80046749109335744362787863728425930400395706369108636286118940773331544031429974807170755380341567420988348901171767865126010764833599924456870392015260929044268704879
g= 45693021002772873526934375989080410698349215636865337756374743694355925509012106847113301513939550485230983070834368143623306972449843954066356179715210603396743992948

A= 13477880666377493172060726278021081223432581331946131324921441001899698080287730543882119267863934261171336505634504705855597201859919914492505663777873336854707427325
B= 25206992152192457764580653092816559945177143797646076230063709560714238855451357472358534406302773784135148174929840524772236209414967913612035949867098878127012797694

encrypted = "67a069ac0fa6cfd91d27ad67b8521ccf4237b89955d2ca89a348151f668bf2b1a49e1a9676780003f8c1d64f55b07262"
a = discrete_log(p, A, g)
shared_key = pow(B, a, p)


def decrypt(shared_key, ct):
    key = sha256(long_to_bytes(shared_key)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(bytes.fromhex(ct)), 16)
    return pt


print(decrypt(shared_key, encrypted))

#flag : Spark{09fdfd8d6cb3b67eade0952540dacf6e4f7fe0fe}
#Author : Quiiper