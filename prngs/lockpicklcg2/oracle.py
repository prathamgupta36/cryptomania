#!/usr/bin/exec-suid -- /usr/bin/python3 -I
import subprocess
from pathlib import Path

LEAK_COUNT = 10


def challenge_dir():
    base = Path("/challenge")
    if base.is_dir():
        return base
    return Path(__file__).resolve().parent


def load_ints(path):
    return [int(line.strip()) for line in path.read_text().splitlines() if line.strip()]


def load_params(path):
    return [int(line.split(": ")[1]) for line in path.read_text().splitlines() if line.strip()]


def print_flag():
    try:
        result = subprocess.run(
            ["cat", "/flag"], capture_output=True, text=True, check=True
        )
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    except Exception:
        print("Flag file is missing or unreadable.")


def submit_solution(expected_m, expected_a, expected_c, expected_outputs):
    try:
        m_guess = int(input("Recovered modulus m: ").strip())
        a_guess = int(input("Recovered multiplier a: ").strip())
        c_guess = int(input("Recovered increment c: ").strip())
    except ValueError:
        print("Try again.")
        return False

    if m_guess != expected_m or a_guess != expected_a or c_guess != expected_c:
        print("Try again.")
        return False

    for i in range(len(expected_outputs)):
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
    leaked_outputs = load_ints(cdir / "leak_outputs")
    expected_outputs = load_ints(cdir / "expected_outputs")
    expected_m = int((cdir / "hidden_modulus").read_text().strip())
    _, expected_a, expected_c = load_params(cdir / "params")

    while True:
        print("\n=== Oracle Menu ===")
        print("1) Leak 10 consecutive outputs")
        print("2) Submit m, a, c, and next 5 outputs")
        print("3) Exit")
        choice = input("> ").strip()

        if choice == "1":
            for i in range(LEAK_COUNT):
                print(f"x{i} = {leaked_outputs[i]}")
        elif choice == "2":
            submit_solution(expected_m, expected_a, expected_c, expected_outputs)
            return
        elif choice == "3":
            print("Bye.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
