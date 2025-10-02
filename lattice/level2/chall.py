#!/usr/bin/exec-suid -- /usr/bin/python3
import sys
from helper import *

EPS = 1e-12 # safety cushion
HR_THRESHOLD = 0.00001337

print("While the team has been exploring the region, they came across our rival division asleep.")

print("This division loves to gives us a hard time.")

print("So, one of the scouts had the great idea of stealing one of their maps and messing with them.")

print("They quietly lifted one of the maps while the other division was dead asleep.")

print("Now it’s time for a prank: we want to hand those rivals back their map, but make it reallllyyy hard to use.\n")


b1, b2 = gen_good_basis()
B = cols_to_matrix(b1, b2)

detB = det2(B)
HR_B = hadamard_ratio(B)

print("=== The Stolen Map ===")
print("Basis representation: COLUMNS. You will input two column vectors, one per line.\n")
print("Here's the clean basis B we swiped:")
print_matrix(B)
print(f"\n|det(B)| = {abs(detB)}")
print(f"HR(B)   = {HR_B:.12f}\n")

print("Your job: submit a new basis B' for the SAME lattice, but skew it so the rivals will hate working with it.")
print("Enter your distorted basis B' (two lines, each 'x y'):")

def read_col(prompt):
    print(prompt, end='', flush=True)
    parts = sys.stdin.readline().strip().split()
    if len(parts) != 2:
        print("Error: need exactly two integers per line.")
        sys.exit(1)
    try:
        x, y = int(parts[0]), int(parts[1])
    except ValueError:
        print("Error: entries must be integers.")
        sys.exit(1)
    return (x, y)

b1p = read_col("b1' = ")
b2p = read_col("b2' = ")
Bp = cols_to_matrix(b1p, b2p)

detBp = det2(Bp)
if detBp == 0:
    print("Rejected: det(B') = 0 (not a basis).")
    sys.exit(0)

adjB = adj2(B)
num = matmul2(adjB, Bp)  
if not divisible(num, detB):
    print("Rejected: B' is not an integer change-of-basis from B.")
    sys.exit(0)

U = [[num[0][0] // detB, num[0][1] // detB],
     [num[1][0] // detB, num[1][1] // detB]]
detU = det2(U)
same_det = (abs(detBp) == abs(detB))
if detU not in (1, -1) or not same_det:
    print("Rejected: B' does not generate the same lattice.")
    sys.exit(0)

HR_Bp = hadamard_ratio(Bp)
print(f"\nResults for your basis B':")
print_matrix(Bp)
print(f"\n|det(B')| = {abs(detBp)}")
print(f"HR(B')   = {HR_Bp:.12f}")

if HR_Bp < HR_THRESHOLD + EPS:
    print("Perfect! The other division will be up all night untangling this one.\n")
    print("Here is a flag for your troubles:")
    with open("/flag", "r") as f:
        print(f.read())
else:
    print("Nah it's still too neat. The prank didn’t land — the map is still easy to work with.")

