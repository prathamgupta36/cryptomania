#!/usr/bin/exec-suid -- /usr/bin/python3
import json, random, sys, os
from math import hypot
import re

ENTRIES_PATH = "challenge_entries"  
REVEAL_ON_FAIL = True

def print_matrix(M):
    max_len = max(len(str(x)) for row in M for x in row)
    for row in M:
        row_str = " ".join(f"{str(x):>{max_len}}" for x in row)
        print(f"[ {row_str} ]")

def extract_entry(entry):
    basis = None; target = None; expected = None
    for k in ("basis","basis_rows","basis_rows_int","basis_rows_flt","B","basis_cols","basis_as_rows"):
        if k in entry: basis = entry[k]; break
    if basis is None and "basis" in entry and isinstance(entry["basis"], dict):
        for k in ("rows","rows_int","rows_flt","R"):
            if k in entry["basis"]: basis = entry["basis"][k]; break
    for k in ("t","target","target_point","pt","point","target_vec","target_coords"):
        if k in entry: target = entry[k]; break
    if target is None and "tx" in entry and "ty" in entry:
        target = [entry["tx"], entry["ty"]]
    for k in ("nearest","nearest_point","expected","closest","p","px_py","closest_point"):
        if k in entry: expected = entry[k]; break
    if expected is None and "px" in entry and "py" in entry:
        expected = [entry["px"], entry["py"]]
    return basis, target, expected

if not os.path.exists(ENTRIES_PATH):
    print(f"Entries file '{ENTRIES_PATH}' not found.", file=sys.stderr)
    sys.exit(1)

entries = []
with open(ENTRIES_PATH, "r") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            f.seek(0)
            try:
                data = json.load(open(ENTRIES_PATH))
                if isinstance(data, list): entries = data
                elif isinstance(data, dict): entries = [data]
                break
            except Exception:
                print("Failed to parse entries file as JSON.", file=sys.stderr)
                sys.exit(1)
            break
if len(entries) == 0:
    print("No entries found in file.", file=sys.stderr)
    sys.exit(1)

rounds = random.randint(32,64)

print("Our intelligence unit has reported that the region ahead is seeded with landmines.")

print("They’ve supplied approximate coordinates of the danger zones, but the readings are imprecise.")

print("Your mission is to snap each coordinate back to the nearest lattice point,")

print("so the Corps can map the true minefield locations and chart a safe path forward.\n")

print(f"There are {rounds} mines\n")

for round_idx in range(1, rounds+1):
    entry = random.choice(entries)
    basis, target, expected = extract_entry(entry)
    if basis is None or target is None or expected is None:
        continue

    print(f"--- Landmine {round_idx}/{rounds} ---")
    print("Basis:")
    print_matrix(basis)
    print("\nMine location = [{:.6f}, {:.6f}]".format(float(target[0]), float(target[1])))

    try:
        guess = input("Submit nearest lattice point as 'u v': ").strip()
    except EOFError:
        sys.exit(0)

    m = re.findall(r"-?\d+", guess)
    if len(m) < 2:
        print("Couldn't parse two integers from input.")
        sys.exit(1)

    sx, sy = int(m[0]), int(m[1])
    px_exp, py_exp = int(expected[0]), int(expected[1])
    dist_sub = hypot(float(target[0]) - sx, float(target[1]) - sy)
    dist_exp = hypot(float(target[0]) - px_exp, float(target[1]) - py_exp)

    if sx == px_exp and sy == py_exp:
        print("Correct!\n")
        if round_idx == rounds:
            print("You found all the bombs. Great Job!")
            print("Here is a flag for your troubles:")
            with open("/flag", "r") as f:
                print(f.read())
    else:
        print("Incorrect.")
        if REVEAL_ON_FAIL:
            print(f"(expected nearest point = [{px_exp}, {py_exp}])\n")
        exit(0)
