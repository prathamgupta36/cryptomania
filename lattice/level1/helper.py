'''
These are janitorial functions. You don't need to understand these to solve the challenge. But its nice to look at them
'''
import os, random, math, sys, time, re
rng = random.Random()

def egcd(a,b):
    if b == 0: return (abs(a), 1 if a>0 else -1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a//b)*y1)

def inv2(M):
    (a,b),(c,d) = M
    det = a*d - b*c
    if abs(det) != 1:
        raise ValueError("not unimodular")
    return (( d//det, -b//det),
            (-c//det,  a//det))

def mul2(A, B):
    return ((A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]),
            (A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]))

def mul2v(A, v):
    return (A[0][0]*v[0] + A[0][1]*v[1],
            A[1][0]*v[0] + A[1][1]*v[1])

def shear_x(k): return ((1,k),(0,1))
def shear_y(k): return ((1,0),(k,1))
def swap():     return ((0,1),(1,0))

def signflip(col):
    if col == 0: return ((-1,0),(0,1))
    else:        return ((1,0),(0,-1))

def sample_hard_reduced():
    for _ in range(10000):
        a = rng.randrange(-20,21)
        b = rng.randrange(-20,21)
        if a == 0 and b == 0: continue
        if math.gcd(a,b) != 1: continue
        n1 = a*a + b*b
        if n1 < 30 or n1 > 900: continue
        if n1 % 2 == 1: continue

        sgn = rng.choice((-1,1))
        t   = sgn*(n1//2 - 1)

        g, x, y = egcd(a, b)
        if t % g != 0: continue
        m = t // g
        c0 = x*m
        d0 = y*m

        best = None
        target_lo = int(math.ceil(1.05 * n1))
        target_hi = int(math.floor(1.12 * n1))
        for k in range(-2000, 2001):
            c = c0 + (b//g)*k
            d = d0 - (a//g)*k
            n2 = c*c + d*d
            if n2 < n1:
                continue
            if n2 >= target_lo and n2 <= target_hi:
                cand = (a,b,c,d,n1,n2)

                if best is None or n2 < best[5]:
                    best = cand
                    if n2 == target_lo:
                        break
        if best is None:
            continue

        a,b,c,d,n1,n2 = best
        dot = a*c + b*d

        if abs(2*dot) <= n1 and abs(2*dot) >= int(0.98*n1):
            return (a,b,c,d)

    raise RuntimeError("failed to sample hard reduced basis; widen ranges")

def print_matrix(M):
    if not M or not all(isinstance(row, list) for row in M):
        print("Invalid matrix format.")
        return

    max_len = max(len(str(x)) for row in M for x in row)

    for row in M:
        row_str = " ".join(f"{str(x):>{max_len}}" for x in row)
        print(f"[ {row_str} ]")

def bad_base_maker():
        U = ((1,0),(0,1))
        ops = rng.randrange(6, 10)
        for _ in range(ops):
            r = rng.random()
            if r < 0.60:
                k = rng.choice((-1,1)) * rng.randrange(150, 600)
                U = mul2(U, shear_x(k) if rng.random()<0.5 else shear_y(k))
            elif r < 0.85:
                U = mul2(U, swap())
            else:
                U = mul2(U, signflip(rng.randrange(2)))
        return U
