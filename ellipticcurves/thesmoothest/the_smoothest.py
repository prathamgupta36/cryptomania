from Crypto.Random.random import getrandbits
from check import out
import json

"""
Elliptic curve math.
'inf' = 0 = O (different notations)
"""

def ec_add(P1, P2, curve):
    if P1 == 'inf': return P2
    if P2 == 'inf': return P1

    x1, y1 = P1
    x2, y2 = P2
    a, b, m = curve
    if x1 == x2 and y1 == (m - y2) % m: return 'inf'
    if P1 != P2:
        L = ((y2 - y1) * pow((x2 - x1), -1, m)) % m
    else:
        L = ((3 * pow(x1, 2) + a) * pow(2 * y1, -1, m)) % m

    x3 = (pow(L, 2) - x1 - x2) % m
    y3 = (L * (x1 - x3) - y1) % m
    return x3, y3


def inv(P, curve):
    a, b, m = curve
    x, y = P
    return (x, m - y)


def ec_mult(P, n, curve):
    neg = False
    if n < 0:
        neg = True
        n = abs(n)
    Q = P
    R = 'inf'
    while n > 0:
        if n % 2 == 1:
            R = ec_add(R, Q, curve)
        Q = ec_add(Q, Q, curve)
        n = n // 2
    return R if not neg else inv(R, curve)


"""
---------- Challenge ----------
"""

def main():

    a, b = 394911, 946268
    p = 293688789654054126296597974208940128669
    curve = (a, b, p)

    G = (
        87374739624386567349158808505363486778,
        88136216566589590724328033328282883270
    ) # generator point

    order_G = 346572432  # hint

    x = getrandbits(128) % order_G
    H = ec_mult(G, x, curve)

    print(f'Your task will be to break this elliptic curve discrete log problem. You are to solve for x in G*x=H.')
    print(f"Here's your data: (G) `{G}`\n(H) `\n{H}`")
    print(f"I will give you this hint: the order of G in the group of the curve, that is, the lowest positive integer such that G*n = 0 is: {order_G}!")


    '''
    checking
    '''
    (t1, t2, t3, t4, t5) = out(x)
    s1 = input("Input factorization dictionary (form { p:e } in json: >")
    assert t1 == json.load(s1)

    s2 = input("Input list of bases of power prime DLP subproblems (json list) >")
    assert t2 == json.loads(s2)

    s3 = input("Input list of h_i values of power prime DLP subproblems (json list) >")
    assert t3 == json.loads(s3)

    s4 = input("Input ")









if __name__ == '__main__':
    main()