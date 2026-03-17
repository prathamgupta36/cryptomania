#!/usr/bin/env python3
import secrets
from pathlib import Path

MASK32 = 0xFFFFFFFF


def challenge_dir():
    base = Path("/challenge")
    if base.is_dir():
        return base
    return Path(__file__).resolve().parent


def choose_seed():
    return secrets.randbelow(MASK32) + 1  # non-zero 32-bit seed


def main():
    cdir = challenge_dir()
    seed = choose_seed()

    (cdir / "super_secret_seed").write_text(f"{seed}\n")

if __name__ == "__main__":
    main()
