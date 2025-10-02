#!/usr/bin/env python3
import math
import random

MIN_COORD = 1_000_000
MAX_COORD = 10_000_000
_rng = random.SystemRandom()
PERTURB = random.randint(MIN_COORD * 2, MAX_COORD // 3)

def print_matrix(M):
    if not M or not all(isinstance(row, list) for row in M):
        print("Invalid matrix format.")
        return

    max_len = max(len(str(x)) for row in M for x in row)

    for row in M:
        row_str = " ".join(f"{str(x):>{max_len}}" for x in row)
        print(f"[ {row_str} ]")

def det2(M):
    return M[0][0]*M[1][1] - M[0][1]*M[1][0]

def adj2(M):
    a, b = M[0]
    c, d = M[1]
    return [[d, -b], [-c, a]]

def matmul2(A, B):
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0],
         A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0],
         A[1][0]*B[0][1] + A[1][1]*B[1][1]],
    ]

def cols_to_matrix(b1, b2):
    return [[b1[0], b2[0]],
            [b1[1], b2[1]]]

def norms_from_columns(M):
    b1 = (M[0][0], M[1][0])
    b2 = (M[0][1], M[1][1])
    n1 = math.hypot(b1[0], b1[1])
    n2 = math.hypot(b2[0], b2[1])
    return n1, n2

def hadamard_ratio(M):
    d = abs(det2(M))
    n1, n2 = norms_from_columns(M)
    if n1 == 0 or n2 == 0:
        return 0.0
    return d / (n1 * n2)

def divisible(M, d):
    return all((M[i][j] % d) == 0 for i in range(2) for j in range(2))


def gen_good_basis():
    while True:
        p = _rng.randint(MIN_COORD, MAX_COORD)
        q = _rng.randint(MIN_COORD, MAX_COORD)
        if p != 0 or q != 0:
            break
    p *= _rng.choice((-1, 1))
    q *= _rng.choice((-1, 1))
    b1 = (p, q)
    b2 = (-q, p)  # start orthogonal

    P = int(PERTURB)
    if P > 0:
        kx = _rng.randint(-P, P)
        ky = _rng.randint(-P, P)
        b2 = (b2[0] + kx, b2[1] + ky)
    return b1, b2
