import random

rng = random.Random()

def identity_matrix(size):
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

def matrix_multiply(A, B):
    rows, inner = len(A), len(A[0])
    cols = len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]

def print_integer_matrix(M):
    if not M:
        print("[]"); return
    width = max(len(str(x)) for row in M for x in row)
    for row in M:
        print("[ " + " ".join(f"{x:>{width}d}" for x in row) + " ]")

def random_unimodular_matrix(size, operations=None):
    if operations is None:
        operations = 5 * size
    U = identity_matrix(size)
    for _ in range(operations):
        r = rng.random()
        if r < 0.65:
            i = rng.randrange(size); j = rng.randrange(size)
            if i == j: continue
            k = rng.choice([-1, 1]) * rng.randint(1, 8)
            for row in range(size):
                U[row][j] += k * U[row][i]
        elif r < 0.85:
            i = rng.randrange(size); j = rng.randrange(size)
            if i == j: continue
            for row in range(size):
                U[row][i], U[row][j] = U[row][j], U[row][i]
        else:
            j = rng.randrange(size)
            for row in range(size):
                U[row][j] = -U[row][j]
    return U

