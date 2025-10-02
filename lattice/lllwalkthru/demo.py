#!/usr/bin/exec-suid -- /usr/bin/python3
from fractions import Fraction
from helper import *
from edit_me import Basis

BASIS = Basis

DELTA = Fraction(3, 4)

def _pause():
    try:
        input("Press Enter to continue to the next round...\n")
    except EOFError:
        pass

print("=== LLL Lattice Reduction Demo ===")
print("\nThis script follows the LLL pseudocode.")

print(">>> Round 0: Initial basis (no operations applied)\n")

print("Basis matrix:")
print_matrix(BASIS)
print()

print("Row norms (squared):")
for i, v in enumerate(BASIS, start=1):
    print(f" ||v{i}||^2 = {squared_norm(v)}")
print()

H0 = hadamard_ratio(BASIS)
print(f"Hadamard ratio H(B) = {H0:.12f}\n")

_pause()

basis = [row[:] for row in BASIS]
n = len(basis)
k = 2
round_idx = 1

while k <= n:
    print(f">>> Round {round_idx}: LLL pseudocode pass at k = {k}\n")

    basis, k_new, did_swap, m_used = lll_pseudocode_pass(basis, k, DELTA)

    v_star, mu_mat = gram_schmidt_with_mu(basis)

    if m_used:
        row_idx_sr = k - 1
        used_pairs = [(j + 1, m) for j, m in enumerate(m_used[:row_idx_sr]) if m != 0]
        if used_pairs:
            parts = ", ".join([f"(j={j}, μ_round={m})" for j, m in used_pairs])
            print("Size reduction:")
            print(f"  on v_{row_idx_sr}: {parts}")
        else:
            print("Size reduction:")
            print(f"  on v_{row_idx_sr}: no changes (all μ rounded to 0)")
    print()

    row_idx_sc = min(max(k - 1, 0), len(basis) - 1)
    sc_entries = size_condition_row(mu_mat, row_idx_sc)
    if sc_entries:
        print(f"Size condition for row v_{row_idx_sc}:")
        for (j, mu_val, holds) in sc_entries:
            flag = "Pass" if holds else "Does Not Pass"
            print(f"  μ_{{{row_idx_sc},{j}}} = {mu_val}   -> {flag}")
    else:
        print(f"Size condition for row v_{row_idx_sc}: (no j<row to check)")
    print()

    lovasz_index = (k_new if did_swap else k_new - 1)
    lovasz_index = max(1, min(lovasz_index, len(basis) - 1))  # clamp

    lhs, rhs, holds = lovasz_values(v_star, mu_mat, lovasz_index, DELTA)
    print(f"Lovász condition at index k={lovasz_index}:")
    print(f"  ||v*_{lovasz_index}||^2               = {lhs}")
    print(f"  (δ - μ^2)·||v*_{lovasz_index-1}||^2  = {rhs}")
    print(f"  Result: {'HOLDS' if holds else 'FAILS'}   (δ = {DELTA})\n")

    if did_swap:
        print("Action: Lovász failed → swapped v_{k-1} and v_k; decremented k.\n")
    else:
        print("Action: Lovász holds  → incremented k.\n")

    print("Current basis matrix:")
    print_matrix(basis)
    print()

    print("Row norms (squared):")
    for i, v in enumerate(basis, start=1):
        print(f"||v{i}||^2 = {squared_norm(v)}")
    print()

    H = hadamard_ratio(basis)
    print(f"Hadamard ratio H(B) = {H:.12f}\n")

    if k_new > n:
        print("Good job following the demo. Here is a flag for your troubles:")
        with open("/flag", "r") as f:
            print(f.read())
        break

    _pause()
    k = k_new
    round_idx += 1
