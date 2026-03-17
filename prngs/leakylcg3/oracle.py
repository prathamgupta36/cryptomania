#!/usr/bin/exec-suid -- /usr/bin/python3 -I
import subprocess
from pathlib import Path

MOD31 = 2147483647


def challenge_dir():
    base = Path("/challenge")
    if base.is_dir():
        return base
    return Path(__file__).resolve().parent


def load_int_file(path):
    return [int(line.strip()) for line in path.read_text().splitlines() if line.strip()]


def normalize_seed(seed):
    seed %= MOD31
    if seed == 0:
        return 1
    return seed


def print_flag():
    try:
        result = subprocess.run(
            ["cat", "/flag"], capture_output=True, text=True, check=True
        )
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    except Exception:
        print("Flag file is missing or unreadable.")


def submit_solution(expected_seed, expected_values):
    try:
        seed_guess = int(input("Recovered seed: ").strip())
    except ValueError:
        print("Try again.")
        return False

    if seed_guess != expected_seed:
        print("Try again.")
        return False

    for i in range(5):
        try:
            guess = int(input(f"output[{i}]: ").strip())
        except ValueError:
            print("Try again.")
            return False
        if guess != expected_values[i]:
            print("Try again.")
            return False

    print("All correct. Printing flag:")
    print_flag()
    return True


def main():
    cdir = challenge_dir()
    expected_seed = normalize_seed(int((cdir / "super_secret_seed").read_text().strip()))
    leaked_sum = int((cdir / "sum_leak").read_text().strip())
    expected_values = load_int_file(cdir / "random")

    while True:
        print("\n=== Oracle Menu ===")
        print("1) Leak sum of two hidden seed-table indices")
        print("2) Submit seed + first 5 outputs")
        print("3) Exit")
        choice = input("> ").strip()

        if choice == "1":
            print(f"seed_table[i] + seed_table[j] = {leaked_sum}")
            print("(i and j are hidden, i != j, both in [1, 30])")
        elif choice == "2":
            submit_solution(expected_seed, expected_values)
            return
        elif choice == "3":
            print("Bye.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
