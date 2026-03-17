#!/usr/bin/env python3
import math
import secrets
from pathlib import Path
from sympy import randprime

LEAK_COUNT = 10
PREDICT_COUNT = 5


def challenge_dir():
    base = Path("/challenge")
    if base.is_dir():
        return base
    return Path(__file__).resolve().parent


def dump_ints(path, values):
    path.write_text("".join(f"{v}\n" for v in values))


def random_31bit_prime():
    return int(randprime(1 << 30, 1 << 31))


def recoverable_modulus_from_outputs(outputs):
    diffs = [outputs[i + 1] - outputs[i] for i in range(len(outputs) - 1)]
    g = 0
    for i in range(len(diffs) - 2):
        z = diffs[i + 2] * diffs[i] - diffs[i + 1] * diffs[i + 1]
        if z != 0:
            g = math.gcd(g, abs(z))
    return g


def choose_instance():
    while True:
        m = random_31bit_prime()
        seed = secrets.randbelow(m - 1) + 1
        a = secrets.randbelow(m - 3) + 2
        c = secrets.randbelow(m - 1) + 1

        x = [seed]
        for _ in range(LEAK_COUNT + PREDICT_COUNT - 1):
            x.append((a * x[-1] + c) % m)

        # Keep instances aligned with intended solve path.
        d1 = (x[1] - x[0]) % m
        if d1 == 0:
            continue
        if math.gcd(d1, m) != 1:
            continue
        if recoverable_modulus_from_outputs(x[:LEAK_COUNT]) != m:
            continue

        return seed, a, c, m, x


def main():
    cdir = challenge_dir()
    seed, a, c, m, outputs = choose_instance()

    dump_ints(cdir / "leak_outputs", outputs[:LEAK_COUNT])
    dump_ints(cdir / "expected_outputs", outputs[LEAK_COUNT:LEAK_COUNT + PREDICT_COUNT])
    (cdir / "hidden_modulus").write_text(f"{m}\n")
    (cdir / "params").write_text(f"seed: {seed}\na: {a}\nc: {c}\n")


if __name__ == "__main__":
    main()
