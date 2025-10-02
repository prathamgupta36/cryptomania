#!/usr/bin/sage 

NUM_ENTRIES   = 100            
LOW           = 10**6         
HIGH          = 10**9         
SEED          = 1337          
OUTPUT_PATH   = "challenge_entries"
NUDGE_FRAC_MIN = 0.01        
NUDGE_FRAC_MAX = 0.03       

import json, math, random, sys
from math import sqrt, pi, cos, sin, hypot
from sage.all import Matrix, ZZ

def dot(a,b): return a[0]*b[0] + a[1]*b[1]
def norm2(a): return dot(a,a)
def norm(a): return sqrt(norm2(a))

def babai_nearest(b1, b2, t):
    den1 = norm2(b1)
    if den1 == 0: return None
    mu21 = dot(b2, b1) / den1
    b2s  = (b2[0] - mu21*b1[0], b2[1] - mu21*b1[1])
    den2 = norm2(b2s)
    if den2 == 0:
        b1, b2 = b2, b1
        den1 = norm2(b1)
        if den1 == 0: return None
        mu21 = dot(b2, b1) / den1
        b2s  = (b2[0] - mu21*b1[0], b2[1] - mu21*b1[1])
        den2 = norm2(b2s)
        if den2 == 0: return None

    
    c2 = (t[0]*b2s[0] + t[1]*b2s[1]) / den2
    k2 = int(round(c2))
    t2 = (t[0] - k2*b2[0], t[1] - k2*b2[1])

    c1 = (t2[0]*b1[0] + t2[1]*b1[1]) / den1
    k1 = int(round(c1))

    px = k1*b1[0] + k2*b2[0]
    py = k1*b1[1] + k2*b2[1]
    return k1, k2, (px, py)

def refine_neighbors(b1, b2, t, k1, k2):
    best = None
    for dk1 in (-1, 0, 1):
        for dk2 in (-1, 0, 1):
            x = k1 + dk1
            y = k2 + dk2
            px = x*b1[0] + y*b2[0]
            py = x*b1[1] + y*b2[1]
            d  = hypot(t[0] - px, t[1] - py)
            if best is None or d < best[0]:
                best = (d, (px, py), (x, y))
    _, pbest, _ = best
    return pbest

def make_instance(rng):
    def rcomp():
        v = rng.randrange(LOW, HIGH+1)
        return v if rng.random() < 0.5 else -v

    B1 = (rcomp(), rcomp())
    k  = 1.0 + 2.0 * rng.random()
    nudge_mag = rng.randrange(LOW//5, LOW)
    nudx = rng.randrange(-nudge_mag, nudge_mag+1)
    nudy = rng.randrange(-nudge_mag, nudge_mag+1)
    B2 = (int(k*B1[0]) + nudx, int(k*B1[1]) + nudy)

    det = B1[0]*B2[1] - B1[1]*B2[0]
    if det == 0:
        B2 = (B2[0] + 1, B2[1] - 1)
        det = B1[0]*B2[1] - B1[1]*B2[0]

    mid = ((B1[0] + B2[0]) / 2.0, (B1[1] + B2[1]) / 2.0)
    frac = NUDGE_FRAC_MIN + (NUDGE_FRAC_MAX - NUDGE_FRAC_MIN) * rng.random()
    step = frac * min(norm(B1), norm(B2))
    phi = 2.0 * pi * rng.random()
    t = (mid[0] + step*cos(phi), mid[1] + step*sin(phi))

    M = Matrix(ZZ, [[int(B1[0]), int(B1[1])],
					[int(B2[0]), int(B2[1])]])
    M_lll = M.LLL()
    r = list(M_lll.rows())
    r1 = (float(r[0][0]), float(r[0][1]))
    r2 = (float(r[1][0]), float(r[1][1]))
    
    res = babai_nearest(r1, r2, t)
    if res is None:
        return None  
    k1, k2, (px_b, py_b) = res
    px, py = refine_neighbors(r1, r2, t, k1, k2)

    a, b = B1[0], B2[0]
    c, d = B1[1], B2[1]
    return {
        "basis_rows": [[a, b], [c, d]],
        "det": int(det),
        "target": [float(t[0]), float(t[1])],
        "nearest_point": [int(px), int(py)],
    }

rng = random.Random(SEED) if SEED is not None else random.SystemRandom()

wrote = 0
with open(OUTPUT_PATH, "w") as f:
    while wrote < NUM_ENTRIES:
        entry = make_instance(rng)
        if entry is None:
            continue
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")
        wrote += 1

print(f"Wrote {wrote} entries to {OUTPUT_PATH}")

