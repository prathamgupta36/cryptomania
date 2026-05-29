from fractions import Fraction
import random
import math

rng = random.Random()

Matrix = list  
Vector = list

def eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def copy_mat(A):
    return [row[:] for row in A]

def transpose(A):
    return [list(col) for col in zip(*A)]

def matmul(A, B):
    r, m = len(A), len(A[0])
    assert m == len(B)
    c = len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(c)] for i in range(r)]

def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

def print_matrix(M):
    if not M:
        print("[]"); return
    width = max(len(str(x)) for row in M for x in row)
    for row in M:
        print("[ " + " ".join(f"{x:>{width}d}" for x in row) + " ]")

def random_unimodular(n, ops_min=None, ops_max=None):
    if ops_min is None:
        ops_min = 3 * n
    if ops_max is None:
        ops_max = 6 * n
    T = eye(n)
    ops = rng.randint(ops_min, ops_max)
    for _ in range(ops):
        r = rng.random()
        if r < 0.60:
            i = rng.randrange(n)
            j = rng.randrange(n)
            if i == j: continue
            k = rng.choice([-1, 1]) * rng.randint(1, 10)
            for row in range(n):
                T[row][j] += k * T[row][i]
        elif r < 0.85:
            i = rng.randrange(n)
            j = rng.randrange(n)
            if i == j: continue
            for row in range(n):
                T[row][i], T[row][j] = T[row][j], T[row][i]
        else:
            j = rng.randrange(n)
            for row in range(n):
                T[row][j] = -T[row][j]
    return T

def invert_unimodular(T):
    n = len(T)
    A = [[Fraction(T[i][j]) for j in range(n)] for i in range(n)]
    Inv = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]

    for c in range(n):
        piv = None
        for r in range(c, n):
            if A[r][c] != 0:
                piv = r; break
        if piv is None:
            raise ValueError("Singular matrix (not unimodular?)")
        if piv != c:
            A[c], A[piv] = A[piv], A[c]
            Inv[c], Inv[piv] = Inv[piv], Inv[c]
        f = A[c][c]
        for j in range(n):
            A[c][j] /= f
            Inv[c][j] /= f
        # eliminate other rows
        for r in range(n):
            if r == c: continue
            mult = A[r][c]
            if mult == 0: continue
            for j in range(n):
                A[r][j] -= mult * A[c][j]
                Inv[r][j] -= mult * Inv[c][j]

    Inv_int = [[int(Inv[i][j]) for j in range(n)] for i in range(n)]
    return Inv_int

def sample_nice_basis(n, start=20, step_min=3, step_max=8):
    B = [[0] * n for _ in range(n)]
    scale = start
    for i in range(n):
        scale += rng.randint(step_min, step_max)
        B[i][i] = scale
    for i in range(n):
        for j in range(i+1, n):
            B[i][j] = rng.randint(-2, 2)
    return B

