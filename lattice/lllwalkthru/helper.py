from typing import List, Tuple
from fractions import Fraction
import math

Vector = List[int]
Basis = List[List[int]]

def dot_product(v: Vector, w: Vector) -> int:
    return sum(vi * wi for vi, wi in zip(v, w))

def squared_norm(v: Vector) -> int:
    return dot_product(v, v)

def nearest_integer_half_away_from_zero(x: Fraction) -> int:
    if x >= 0:
        n = int(x)  # floor
        frac = x - n
        return n if frac < Fraction(1, 2) else n + 1
    else:
        n = int(math.floor(float(x)))  # ensure <= x
        pos = -x
        m = nearest_integer_half_away_from_zero(pos)
        return -m

def subtract_integer_multiple(v: Vector, m: int, w: Vector) -> Vector:
    return [vi - m * wi for vi, wi in zip(v, w)]


def det_bareiss_int(matrix: Basis) -> int:
    n = len(matrix)
    A = [row[:] for row in matrix]
    denom = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            for r in range(k + 1, n):
                if A[r][k] != 0:
                    A[k], A[r] = A[r], A[k]
                    break
        pivot = A[k][k]
        if pivot == 0:
            return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * pivot - A[i][k] * A[k][j]) // (denom if denom != 0 else 1)
            A[i][k] = 0
        denom = pivot
    return A[-1][-1]

def hadamard_ratio(basis: Basis) -> float:
    det_abs = abs(det_bareiss_int(basis))
    if det_abs == 0:
        return 0.0
    prod_norms = 1.0
    for v in basis:
        prod_norms *= math.sqrt(float(squared_norm(v)))
        if prod_norms == 0.0:
            return 0.0
    return float(det_abs) / prod_norms



def gram_schmidt_with_mu(basis: Basis) -> Tuple[List[List[Fraction]], List[List[Fraction]]]:
    n = len(basis)
    v_star: List[List[Fraction]] = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    mu: List[List[Fraction]] = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    for i in range(n):
        # start with vi
        vi = [Fraction(x) for x in basis[i]]
        # subtract projections onto previous v_star
        for j in range(i):
            denom = sum(v_star[j][t] * v_star[j][t] for t in range(n))
            if denom == 0:
                mu_ij = Fraction(0)
            else:
                numer = sum(vi[t] * v_star[j][t] for t in range(n))
                mu_ij = numer / denom
            mu[i][j] = mu_ij
            for t in range(n):
                vi[t] -= mu_ij * v_star[j][t]
        v_star[i] = vi
    return v_star, mu

def size_reduce_row_k(basis: Basis, mu: List[List[Fraction]], k: int) -> Tuple[Basis, List[int]]:
    n = len(basis)
    m_used = [0] * n
    for j in range(k):
        if j == k:
            break
        m = nearest_integer_half_away_from_zero(mu[k][j])
        m_used[j] = m
        if m != 0:
            basis[k] = subtract_integer_multiple(basis[k], m, basis[j])
    return basis, m_used

def lovasz_holds(v_star: List[List[Fraction]], mu: List[List[Fraction]], k: int, delta: Fraction) -> bool:
    if k <= 0:
        return True
    nrm_k = sum(x * x for x in v_star[k])
    nrm_prev = sum(x * x for x in v_star[k - 1])
    mu_sq = mu[k][k - 1] * mu[k][k - 1]
    return nrm_k >= (delta - mu_sq) * nrm_prev

def lll_pseudocode_pass(basis: Basis, k: int, delta: Fraction = Fraction(3, 4)) -> Tuple[Basis, int, bool, List[int]]:
    n = len(basis)
    if not (2 <= k <= n):
        return basis, k, False, []

    # Fresh GS and mu for current basis
    v_star, mu = gram_schmidt_with_mu(basis)

    # Size reduction on row k-1 (0-indexed: row index = k-1)
    row = k - 1
    basis, m_used = size_reduce_row_k(basis, mu, row)

    # Recompute GS/mu after size reduction
    v_star, mu = gram_schmidt_with_mu(basis)

    # Lovász check between rows k-1 and k-2 (if k>1)
    did_swap = False
    if row >= 1 and not lovasz_holds(v_star, mu, row, delta):
        # swap v_{k-1} and v_{k-2}
        basis[row - 1], basis[row] = basis[row], basis[row - 1]
        did_swap = True
        k = max(k - 1, 2)
    else:
        k = k + 1

    return basis, k, did_swap, m_used

def size_condition_row(mu: List[List[Fraction]], k_row: int) -> List[Tuple[int, Fraction, bool]]:
    out = []
    for j in range(k_row):
        mu_kj = mu[k_row][j]
        holds = abs(mu_kj) <= Fraction(1, 2)
        out.append((j, mu_kj, holds))
    return out

def size_condition_all(mu: List[List[Fraction]]) -> bool:
    n = len(mu)
    for i in range(n):
        for j in range(i):
            if abs(mu[i][j]) > Fraction(1, 2):
                return False
    return True



def lovasz_values(v_star: List[List[Fraction]], mu: List[List[Fraction]], k_row: int, delta: Fraction) -> Tuple[Fraction, Fraction, bool]:
    if k_row <= 0:
        return Fraction(0), Fraction(0), True
    nrm_k = sum(x * x for x in v_star[k_row])
    nrm_prev = sum(x * x for x in v_star[k_row - 1])
    mu_sq = mu[k_row][k_row - 1] * mu[k_row][k_row - 1]
    rhs = (delta - mu_sq) * nrm_prev
    lhs = nrm_k
    return lhs, rhs, lhs >= rhs

def print_matrix(M):
    if not M or not all(isinstance(row, list) for row in M):
        print("Invalid matrix format.")
        return
    max_len = max(len(str(x)) for row in M for x in row)
    for row in M:
        row_str = " ".join(f"{str(x):>{max_len}}" for x in row)
        print(f"[ {row_str} ]")

