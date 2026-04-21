# helper.py
from random import randint
from math import isqrt

class Point:
    def __init__(self, curve, x=None, y=None, inf=False):
        self.curve = curve
        self.inf = inf
        self.x = x
        self.y = y
        if not self.inf and not curve.testPoint(self.x, self.y):
            raise Exception(f"The given point {self} is not on the curve {curve}")

    def __str__(self):
        if self.inf:
            return "INF"
        return f"({self.x}, {self.y})"

class ECC:
    def __init__(self, p: int, a: int, b: int):
        self.p = p
        self.a = a % p
        self.b = b % p

    def testPoint(self, x: int, y: int) -> bool:
        p = self.p
        return (y * y - (x * x * x + self.a * x + self.b)) % p == 0

    def __str__(self):
        return f"y^2 = x^3 + ax + b (mod p)"

def inv_mod(x: int, p: int) -> int:
    x %= p
    if x == 0:
        raise ZeroDivisionError("no inverse")
    return pow(x, p - 2, p)

def neg_point(P: Point) -> Point:
    if P.inf:
        return P
    return Point(P.curve, P.x, (-P.y) % P.curve.p)

def ecc_addition(curve: ECC, P: Point, Q: Point) -> Point:
    p = curve.p

    if P.inf:
        return Q
    if Q.inf:
        return P

    if P.x == Q.x and (P.y + Q.y) % p == 0:
        return Point(curve, inf=True)

    if P.x == Q.x and P.y == Q.y:
        if P.y % p == 0:
            return Point(curve, inf=True)
        lam = ((3 * P.x * P.x + curve.a) * inv_mod(2 * P.y, p)) % p
    else:
        lam = ((Q.y - P.y) * inv_mod(Q.x - P.x, p)) % p

    rx = (lam * lam - P.x - Q.x) % p
    ry = (lam * (P.x - rx) - P.y) % p
    return Point(curve, rx, ry)

def scalar_mul(curve: ECC, P: Point, k: int) -> Point:
    if k < 0:
        raise ValueError("k must be non-negative")
    R = Point(curve, inf=True)
    Q = P
    while k > 0:
        if k & 1:
            R = ecc_addition(curve, R, Q)
        k >>= 1
        if k:
            Q = ecc_addition(curve, Q, Q)
    return R

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = isqrt(n)
    f = 3
    while f <= r:
        if n % f == 0:
            return False
        f += 2
    return True

def rand_prime(lo: int, hi: int) -> int:
    while True:
        p = randint(lo, hi)
        if p % 4 != 3:
            continue
        if is_prime(p):
            return p

def legendre_symbol(a: int, p: int) -> int:
    return pow(a % p, (p - 1) // 2, p)

def sqrt_mod_p(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return 0
    if legendre_symbol(a, p) != 1:
        return None
    y = pow(a, (p + 1) // 4, p)
    if (y * y) % p == a:
        return y
    return None

def nonsingular(curve: ECC) -> bool:
    p = curve.p
    disc = (4 * pow(curve.a, 3, p) + 27 * pow(curve.b, 2, p)) % p
    return disc != 0
