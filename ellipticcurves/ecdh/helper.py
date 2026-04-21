#!/usr/bin/exec-suid -- /usr/bin/python3

def inv_mod(x, p):
    return pow(x, p - 2, p)

def is_on_curve(x, y, p, a, b):
    if x is None or y is None:
        return False
    lhs = (y * y) % p
    rhs = (pow(x, 3, p) + a * x + b) % p
    return lhs == rhs

def ecc_add(P1, P2, p, a):
    if P1 is None: return P2
    if P2 is None: return P1
    
    x1, y1 = P1
    x2, y2 = P2
    
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    
    if x1 == x2 and y1 == y2:
        numerator = (3 * x1 * x1 + a) % p
        denominator = inv_mod(2 * y1, p)
    else:
        numerator = (y2 - y1) % p
        denominator = inv_mod(x2 - x1, p)
        
    lam = (numerator * denominator) % p
    
    xr = (lam * lam - x1 - x2) % p
    yr = (lam * (x1 - xr) - y1) % p
    
    return (xr, yr)

def scalar_mul(Point, k, p, a):
    result = None
    addend = Point
    
    while k > 0:
        if k & 1:
            result = ecc_add(result, addend, p, a)
        addend = ecc_add(addend, addend, p, a)
        k >>= 1
        
    return result
