#!/usr/bin/exec-suid -- /usr/bin/python3
import os, random, math, sys, time, re
from helper import *  

seed = random.random() 
rng = random.Random(seed)

print("You’ve just been recruited into the Expeditionary Survey Corps.\n")
print("Your first assignment: recover the coordinates of a lost supply shipment from a distorted 2D terrain grid.\n")
print("The scouts left behind a lattice, but their base measurements are skewed.\n")
print("Fortunately, with some careful adjustments you should be able to realign the grid.\n")

a, b, c, d = sample_hard_reduced()
B_good = ((a, c), (b, d))

u = rng.randrange(-100, 101)
v = rng.randrange(-100, 101)
if (u, v) == (0, 0):
    v = 1
k_small = (u, v)

U = bad_base_maker()
B_bad = mul2(B_good, U)
U_inv = inv2(U)
c_bad = mul2v(U_inv, k_small)

print("B = ")
print_matrix([list(row) for row in B_bad])

print("\nc = ")
print(f"[{c_bad[0]} {c_bad[1]}]\n")

print("What are the correct coordinates?")

def same_up_to_sign(x, y):
    return x == y or x == -y

try:
    guess = input("\nSubmit your recovered coordinates as 'u v': ").strip()
    nums = re.findall(r"-?\d+", guess)
    if len(nums) >= 2:
        gu, gv = int(nums[0]), int(nums[1])
        ok = same_up_to_sign(gu, u) and same_up_to_sign(gv, v)
        if not ok:
            print("\nNope. That’s not it.")
            sys.exit(0)
    else:
        print("\nCouldn't parse two integers. Example: 17 -9")
        sys.exit(0)
except EOFError:
    sys.exit(0)

while True:
    u2 = rng.randrange(-250, 251)
    v2 = rng.randrange(-250, 251)
    if (u2, v2) != (0, 0):
        break
k2 = (u2, v2)
c2 = mul2v(U_inv, k2)

print("\nWell done. The expedition just realized they misplaced *another* shipment.")
print("Guess who’s stuck finding it? :)\n")
print(f"c2 =\n[{c2[0]} {c2[1]}] ") 

try:
    guess2 = input("\nSubmit your recovered coordinates as 'u v': ").strip()
    gnums = re.findall(r"-?\d+", guess2)
    if len(gnums) >= 2:
        gu, gv = int(gnums[0]), int(gnums[1])
        ok = same_up_to_sign(gu, u2) and same_up_to_sign(gv, v2)
        if not ok:
            print("\nNope. That’s not the correct point.")
            sys.exit(0)
    else:
        print("\nCouldn't parse two integers. Example: 17 -9")
        sys.exit(0)
except EOFError:
    sys.exit(0)

print("\nNow that you’ve shown your skills, the Corps has decided to entrust you with more maps to fix.")
print("These ones cover far larger regions, and the distortions are much more severe :(\n")

num_coords = rng.randrange(50, 101)
print(f"Batch request: recover {num_coords} additional coordinates.\n")

def same_up_to_sign(x, y):
    return x == y or x == -y

for i in range(1, num_coords + 1):
    print("=" * 60)
    print(f"Coordinate {i}/{num_coords}:\n")

    a, b, c, d = sample_hard_reduced()
    B_good = ((a, c), (b, d))

    scale = rng.randrange(10**6, 10**9)
    B_good = (
        (B_good[0][0] * scale, B_good[0][1] * scale),
        (B_good[1][0] * scale, B_good[1][1] * scale),
    )

    U = bad_base_maker()
    B_bad = mul2(B_good, U)
    U_inv = inv2(U)

    u = rng.randrange(-10**6, 10**6)
    v = rng.randrange(-10**6, 10**6)
    if (u, v) == (0, 0):
        v = 1
    k = (u, v)
    c_vec = mul2v(U_inv, k)

    print("B =")
    print_matrix([list(row) for row in B_bad])

    print("\nc =")
    print(f"[{c_vec[0]} {c_vec[1]}]\n")

    guess_loop = input("Submit your recovered coordinates as 'u v': ").strip()
    nums_loop = re.findall(r"-?\d+", guess_loop)
    if len(nums_loop) >= 2:
        gu, gv = int(nums_loop[0]), int(nums_loop[1])

        ok = same_up_to_sign(gu, u) and same_up_to_sign(gv, v)

        if not ok:
            print("\nNope. That’s not it. Expedition aborted.\n")
            sys.exit(0)
    else:
        print("\nCouldn't parse two integers. Example: 123 -456")
        sys.exit(0)

print("Good Job! Here is a flag for your troubles.")
with open("/flag", 'r') as f:
    print(f.read())

