#!/usr/bin/exec-suid -- /usr/bin/python3
import re, random
from helper import *

rounds = random.randint(15, 30)

print("\n\n\t\tMight Wanna resize your window for this one\n\n\n")

input()
print("=== Expeditionary Survey Corps — Hypercube Mission ===\n")
print("Congrats rookie, word got around you survived the last training maps without blowing yourself up.")
print("Naturally, command decided that means you’re ready for the *harder* maps. Don’t thank them all at once.")
print("Here’s your next set of scrambled coordinates. Good luck… you’ll need it.\n")

for r in range(1, rounds + 1):
    n = random.randint(10, 30)

    B_good = sample_nice_basis(n)

    z = [rng.randint(-50, 50) for _ in range(n)]
    if all(x == 0 for x in z):
        z[0] = 1

    v = matvec(B_good, z)

    U = random_unimodular(n)
    B_bad = matmul(B_good, U)

    U_inv = invert_unimodular(U)
    c = matvec(U_inv, z)

    print(f"Dimension n = {n}\n")
    print("Scrambled basis B:")
    print_matrix(B_bad)

    print("\nTransformed vector c:")
    print("[ " + " ".join(str(int(x)) for x in c) + " ]\n")
    print("Submit k as 'k1 k2 ... kn':")

    line = input()
    if not line:
        print("\nNo input.")
        exit(0)

    nums = re.findall(r"-?\d+", line)
    if len(nums) != n:
        print(f"\nExpected {n} integers.")
        exit(0)

    guess = [int(x) for x in nums]

    if guess == v:
        print("\nCorrect. Supplies recovered.\n")
    else:
        print("\nIncorrect.")
        exit(0)

print("Here is a flag for your troubles:")
with open("/flag", "r") as f:
	print(f.read())

