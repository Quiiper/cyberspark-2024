

'''
a and b in not given in this task but since we have two points we can calculate them . Also we will notice that that this is a singular elliptic curve.
This paper and the article will pretty much explain this attack and why we shouldn't use singular elliptic curves.
https://web.northeastern.edu/dummit/docs/numthy_7_elliptic_curves.pdf
https://www.quora.com/For-an-elliptic-curve-in-the-form-Y-2-X-3+AX+B-why-is-4A-3+27B-2-neq-0-the-condition-for-non-singularity'''




from sage.all import *
from Crypto.Util.number import *
p = 4368590184733545720227961182704359358435747188309319510520316493183539079703
F = GF(p)

gx = 8742397231329873984594235438374590234800923467289367269837473862487362482
gy = 225987949353410341392975247044711665782695329311463646299187580326445253608

px=2783008386658980181719333647637994712382488380247652187452669301800415779801
py=1298478436807006620985453010331310673949900432047208612713537702938793467218

M = Matrix(F, [[gx, 1],[px, 1]])
a, b = M.solve_right(vector([gy ** 2 - gx ** 3, py ** 2 - px ** 3]))

assert 4 * a ** 3 + 27 * b ** 2 == 0

x = PolynomialRing(F, 'x').gen()
f = x ** 3 + a * x + b
roots = f.roots()
if roots[0][1] == 1:
    beta, alpha = roots[0][0], roots[1][0]
else:
    alpha, beta = roots[0][0], roots[1][0]
slope = (alpha - beta).sqrt()
u = (gy + slope * (gx - alpha)) / (gy - slope * (gx - alpha))
v = (py + slope * (px - alpha)) / (py - slope * (px - alpha))

flag = discrete_log(v, u)
print(long_to_bytes(flag))


#flag : Spark{S1ngl4r_3CC_Vulnr4bl3}
#Author : Quiiper