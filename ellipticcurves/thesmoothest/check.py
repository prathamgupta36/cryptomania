import sys
from math import floor, ceil, sqrt
from sympy.ntheory.modular import crt
import json


def ec_add_naive(P1, P2, curve):
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


def ec_add_multiple_naive(points, curve):
    acc = points[0]
    m = curve[2]
    for p in points[1:]:
        acc = ec_add_naive(acc, p, curve)
    # acc = (acc[0]%m, acc[1]%m)
    return acc


def inv(P, curve):
    a, b, m = curve
    x, y = P
    return (x, m - y)


def ec_mult_naive(P, n, curve):
    neg = False
    if n < 0:
        neg = True
        n = abs(n)
    Q = P
    R = 'inf'
    while n > 0:
        if n % 2 == 1:
            R = ec_add_naive(R, Q, curve)
        Q = ec_add_naive(Q, Q, curve)
        n = n // 2
    return R if not neg else inv(R, curve)




def validate(P, curve):
    x, y = P
    a, b, m = curve
    return pow(y, 2, m) == (pow(x, 3, m) + a * x + b) % m



def dl_composite(g, N, h, ops):
    # solve for x in g^x=h when N := ord(g) factorable into small primes
    gr_op, gr_pow = ops

    fact_dict = factor(N)  # { prime : power }
    gis = [gr_pow(g, N // (q ** e)) for q, e in fact_dict.items()]
    his = [gr_pow(h, N // (q ** e)) for q, e in fact_dict.items()]


    ys = [dl_prime_power(gis[i], his[i], q, e, ops) for i, (q, e) in enumerate(fact_dict.items())]

    mods = [q ** e for q, e in fact_dict.items()]
    x = crt(mods, ys)
    return x


def dl_prime_power(g, h, q, e, ops):
    # solve for x in g^x=h when ord(g) = q^e for q prime
    gr_op, gr_pow = ops
    xis = [0] * e

    for i in range(1, e + 1):
        gi = gr_pow(g, (q ** (e - 1)))
        hi = gr_pow(gr_op(h,
                          gr_pow(g, (- sum([xj * q ** j for j, xj in enumerate(xis[:i])])))
                          ),
                    (q ** (e - i))
                    )
        xis[i - 1] = dl_prime(gi, hi, q, ops)

    print('x_i set: ', xis)
    return sum([xi * q ** j for j, xi in enumerate(xis)])


def dl_prime(g, h, q, ops):
    gr_op, gr_pow = ops
    gcur = 'inf'
    for i in range(0, q):
        if gcur == h:
            return i
        gcur = gr_op(gcur, g)


def factor(n):
    # brute force, only small n
    u = floor(sqrt(n))
    d = {}
    for i in range(2, u):
        count = 0
        while n % i == 0:
            count += 1
            n = n // i
        if count > 0: d[i] = count
    return d



def out(x):
    a, b = (394911, 946268)
    p = 293688789654054126296597974208940128669
    E = (a, b, p)
    ops = (lambda a, b: ec_add_naive(a, b, E), lambda a, n: ec_mult_naive(a, n, E))
    gr_op, gr_pow = ops
    g = (87374739624386567349158808505363486778, 88136216566589590724328033328282883270)
    ordG = 346572432
    assert validate(g,E)

    h = gr_pow(g,x)
    assert validate(h, E)


    fact_dict = factor(ordG)  # { prime : power }
    gis = [gr_pow(g, ordG // (q ** e)) for q, e in fact_dict.items()]
    his = [gr_pow(h, ordG // (q ** e)) for q, e in fact_dict.items()]

    ys = [dl_prime_power(gis[i], his[i], q, e, ops) for i, (q, e) in enumerate(fact_dict.items())]

    mods = [q ** e for q, e in fact_dict.items()]

    out_x = crt(mods, ys)
    return (fact_dict, gis, his, ys, out_x)





