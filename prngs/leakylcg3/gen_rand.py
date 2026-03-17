#!/usr/bin/env python3
import secrets
from pathlib import Path

MOD31 = 2147483647  # 2^31 - 1
PM_A = 16807


def challenge_dir():
    base = Path("/challenge")
    if base.is_dir():
        return base
    return Path(__file__).resolve().parent


def normalize_seed(seed):
    seed %= MOD31
    if seed == 0:
        return 1
    return seed


def glibc_random_outputs(seed, count):
    needed = 344 + count
    r = [0] * needed
    r[0] = seed

    for i in range(1, 31):
        r[i] = (PM_A * r[i - 1]) % MOD31

    initial_seed_table = r[:31]

    for i in range(31, 34):
        r[i] = r[i - 31]

    for i in range(34, needed):
        r[i] = (r[i - 31] + r[i - 3]) & 0xFFFFFFFF

    outputs = []
    for i in range(344, 344 + count):
        outputs.append((r[i] & 0xFFFFFFFF) >> 1)
    return initial_seed_table, outputs


def load_seed(path):
    return int(path.read_text().strip())


def dump_ints(path, values):
    path.write_text("".join(f"{v}\n" for v in values))


def random_pair_1_to_30():
    i = secrets.randbelow(30) + 1
    j = secrets.randbelow(30) + 1
    while j == i:
        j = secrets.randbelow(30) + 1
    if i > j:
        i, j = j, i
    return i, j


def main():
    cdir = challenge_dir()
    raw_seed = load_seed(cdir / "super_secret_seed")
    seed = normalize_seed(raw_seed)

    initial_seed_table, outputs = glibc_random_outputs(seed, 5)

    leak_i, leak_j = random_pair_1_to_30()
    leaked_sum = initial_seed_table[leak_i] + initial_seed_table[leak_j]

    dump_ints(cdir / "seed_table", initial_seed_table)
    dump_ints(cdir / "random", outputs)
    (cdir / "sum_leak").write_text(f"{leaked_sum}\n")

    # Helpful for local debugging; not needed by solver/oracle.
    #(cdir / "debug_pair").write_text(f"{leak_i} {leak_j}\n")


if __name__ == "__main__":
    main()
