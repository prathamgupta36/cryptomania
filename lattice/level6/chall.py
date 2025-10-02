#!/usr/bin/exec-suid -- /usr/bin/python3
import sys
import re
from helper import * 

MAX_ATTEMPTS = 3

print("=== Expeditionary Survey Corps — SVP Warmup (multi-round) ===\n")
print("Survive the rounds. Each round has a random dimension; pass them all to earn the flag.\n")

ROUNDS = 1 # more rounds is just pain :( 

for round_idx in range(1, ROUNDS + 1):
    dimension = rng.randint(10, 30)
    print(f"--- Round {round_idx}/{ROUNDS} (dimension = {dimension}) ---\n")

    diagonal_basis = [[0] * dimension for _ in range(dimension)]
    value = rng.randint(400, 800)
    for i in range(dimension):
        value += rng.randint(20, 40)
        diagonal_basis[i][i] = value

    short_vector = [rng.randint(-20, 20) for _ in range(dimension)]
    if all(x == 0 for x in short_vector):
        short_vector[0] = 1

    offset_vector = [rng.randint(-5, 5) for _ in range(dimension)]
    offset_vector[dimension - 1] = 0
    planted_column = [
        short_vector[i] + diagonal_basis[i][i] * offset_vector[i] for i in range(dimension)
    ]

    good_basis = [row[:] for row in diagonal_basis]
    for i in range(dimension):
        good_basis[i][dimension - 1] = planted_column[i]

    scrambling_matrix = random_unimodular_matrix(dimension)
    scrambled_basis = matrix_multiply(good_basis, scrambling_matrix)

    print(f"Dimension n = {dimension}\n")
    print("Scrambled basis B:")
    print_integer_matrix(scrambled_basis)

    print("\nSubmit the shortest nonzero lattice vector v as 'v1 v2 ... vn':", flush=True)

    correct = False
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            line = input()
        except EOFError:
            print("\nIncorrect.", flush=True)
            print("Planted short vector was:", short_vector, flush=True)
            sys.exit(0)

        if not line:
            if attempt < MAX_ATTEMPTS:
                print(f"Not valid. Attempts left: {MAX_ATTEMPTS - attempt}", flush=True)
                continue
            else:
                print("\nIncorrect.", flush=True)
                print("Planted short vector was:", short_vector, flush=True)
                sys.exit(0)

        nums = re.findall(r"-?\d+", line)
        if len(nums) != dimension:
            if attempt < MAX_ATTEMPTS:
                print(f"Not valid. Attempts left: {MAX_ATTEMPTS - attempt}", flush=True)
                continue
            else:
                print("\nIncorrect.", flush=True)
                print("Planted short vector was:", short_vector, flush=True)
                sys.exit(0)

        submitted_vector = [int(x) for x in nums]
        is_negative = all(submitted_vector[i] == -short_vector[i] for i in range(dimension))

        if submitted_vector == short_vector or is_negative:
            print("\nCorrect for this round.\n", flush=True)
            correct = True
            break
        else:
            if attempt < MAX_ATTEMPTS:
                print(f"Incorrect. Attempts left: {MAX_ATTEMPTS - attempt}", flush=True)
            else:
                print("\nIncorrect.", flush=True)
                print("Planted short vector was:", short_vector, flush=True)
                sys.exit(0)

    if not correct:
        sys.exit(0)

print("\nWell done, you passed every round.")
print("Here is a flag for your troubles:")

with open("/flag", "r") as f:
	print(f.read())

