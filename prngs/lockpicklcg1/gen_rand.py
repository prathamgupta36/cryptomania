#!/usr/bin/env python3
import secrets
from pathlib import Path

MODULUS = 2147483647  # prime: 2^31 - 1


def challenge_dir():
    base = Path("/challenge")
    if base.is_dir():
        return base
    return Path(__file__).resolve().parent


def dump_ints(path, values):
    path.write_text("".join(f"{v}\n" for v in values))


def choose_instance():
    while True:
        seed = secrets.randbelow(MODULUS - 1) + 1
        a = secrets.randbelow(MODULUS - 3) + 2  # [2, MODULUS-2]
        c = secrets.randbelow(MODULUS - 1) + 1  # [1, MODULUS-1]

        x = [seed]
        for _ in range(7):
            x.append((a * x[-1] + c) % MODULUS)

        # Require invertible denominator for straightforward intended solve.
        if (x[1] - x[0]) % MODULUS != 0:
            return seed, a, c, x


def main():
    cdir = challenge_dir()
    seed, a, c, outputs = choose_instance()

    (cdir / "modulus").write_text(f"{MODULUS}\n")
    dump_ints(cdir / "leak_outputs", outputs[:3])      # x0, x1, x2
    dump_ints(cdir / "expected_outputs", outputs[3:8])  # x3..x7
    (cdir / "params").write_text(f"seed: {seed}\na: {a}\nc: {c}\n")


if __name__ == "__main__":
    main()
