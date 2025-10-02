#!/usr/bin/exec-suid -- /usr/bin/python3
from helper import * 
from edit_me import basis

# ---------------- CONFIGURE THIS IF YOU WANT TO VIEW A DIFFERENT BASIS ----------------
V1 = basis[0] 
V2 = basis[1] 

def _pause():
    input("Press Enter to continue to the next round...")

print("=== Gaussian Lattice Reduction Demo ===")
print("This script follows the pseudocode for 2D Gauss reduction.")

print(">>> Round 0: Initial basis")
angle0 = angle_degrees_between(V1, V2)

print("\nBasis matrix:")
print_matrix([[V1[0], V1[1]], [V2[0], V2[1]]])

print("\nBasis Norms:")
print(f"v1 = {V1}   ||v1||^2 = {squared_norm_2d(V1)}")
print(f"v2 = {V2}   ||v2||^2 = {squared_norm_2d(V2)}")

print(f"\nInitial angle(v1, v2) = {angle0:.12f}°\n")

_pause()

v1, v2 = V1, V2
round_idx = 1

while True:
    v1, v2, mu, swapped = gauss_pseudocode_pass(v1, v2)

    print(f">>> Round {round_idx}: Applying Gauss lattice reduction algo\n")
    if swapped:
        print("Step 1: Swapped v1 and v2 because ||v2|| < ||v1||")
    print(f"Step 2: Computed μ = {mu}")
    print("Step 3: Updated v2 := v2 - μ*v1\n")

    print("Basis matrix:")
    print_matrix([[v1[0], v1[1]], [v2[0], v2[1]]])

    print("\nBasis Norms:")
    print(f"v1 = {v1}   ||v1||^2 = {squared_norm_2d(v1)}")
    print(f"v2 = {v2}   ||v2||^2 = {squared_norm_2d(v2)}")

    angle_deg = angle_degrees_between(v1, v2)
    print(f"\nangle(v1, v2) = {angle_deg:.12f}°\n")

    if mu == 0:
        print("Good job following the demo. Here is a flag for your troubles:")
        with open("/flag", "r") as f:
            print(f.read())
        break

    round_idx += 1
    _pause()
