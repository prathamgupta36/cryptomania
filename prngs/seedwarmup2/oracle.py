#!/usr/bin/exec-suid -- /usr/bin/python3 -I
import subprocess
from pathlib import Path

MASK32 = 0xFFFFFFFF
PREDICT_COUNT = 5


def challenge_dir():
    base = Path("/challenge")
    if base.is_dir():
        return base
    return Path(__file__).resolve().parent


def xorshift32(state):
    state ^= (state << 13) & MASK32
    state ^= (state >> 17) & MASK32
    state ^= (state << 5) & MASK32
    return state & MASK32


def derive_outputs(seed, count):
    out = []
    cur = seed
    for _ in range(count):
        cur = xorshift32(cur)
        out.append(cur)
    return out


def print_flag():
    try:
        result = subprocess.run(
            ["cat", "/flag"], capture_output=True, text=True, check=True
        )
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    except Exception:
        print("Flag file is missing or unreadable.")


def submit_solution(expected_seed, expected_outputs):
    try:
        seed_guess = int(input("Recovered initial seed s0: ").strip())
    except ValueError:
        print("Try again.")
        return False

    if seed_guess != expected_seed:
        print("Try again.")
        return False

    for i in range(PREDICT_COUNT):
        try:
            guess = int(input(f"next_output[{i}]: ").strip())
        except ValueError:
            print("Try again.")
            return False
        if guess != expected_outputs[i]:
            print("Try again.")
            return False

    print("All correct. Printing flag:")
    print_flag()
    return True


def main():
    cdir = challenge_dir()
    expected_seed = int((cdir / "super_secret_seed").read_text().strip())
    outputs = derive_outputs(expected_seed, PREDICT_COUNT + 1)
    leak = outputs[0]
    expected_outputs = outputs[1:]

    while True:
        print("\n=== Oracle Menu ===")
        print("1) Leak one output")
        print("2) Submit recovered seed and next 5 outputs")
        print("3) Exit")
        choice = input("> ").strip()

        if choice == "1":
            print("[info] xorshift32 uses:")
            print("       x ^= x << 13; x ^= x >> 17; x ^= x << 5")
            print(f"x1 = {leak}")
        elif choice == "2":
            submit_solution(expected_seed, expected_outputs)
            return
        elif choice == "3":
            print("Bye.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
