#!/usr/bin/exec-suid -- /usr/bin/python3 -I
import secrets
import subprocess

MASK32 = 0xFFFFFFFF
PREDICT_COUNT = 5
QUERY_BUDGET = 32


def xorshift32(state, a, b, c):
    state ^= (state << a) & MASK32
    state ^= (state >> b) & MASK32
    state ^= (state << c) & MASK32
    return state & MASK32


def derive_outputs(seed, a, b, c, count):
    outputs = []
    cur = seed
    for _ in range(count):
        cur = xorshift32(cur, a, b, c)
        outputs.append(cur)
    return outputs


def choose_seed():
    return secrets.randbelow(MASK32) + 1


def choose_params():
    a = secrets.randbelow(31) + 1
    b = secrets.randbelow(31) + 1
    c = secrets.randbelow(31) + 1
    return a, b, c


def print_flag():
    try:
        result = subprocess.run(
            ["cat", "/flag"], capture_output=True, text=True, check=True
        )
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    except Exception:
        print("Flag file is missing or unreadable.")


def submit_solution(expected_outputs):
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
    seed = choose_seed()
    a, b, c = choose_params()

    leaked_output = derive_outputs(seed, a, b, c, PREDICT_COUNT + 1)
    x1 = leaked_output[0]
    expected_outputs = leaked_output[1:]
    queries_left = QUERY_BUDGET
    leak_revealed = False

    while True:
        print("\n=== Oracle Menu ===")
        print(f"1) Query the hidden one-step transition ({queries_left} queries left)")
        print("2) End query phase and leak one output from the secret stream")
        print("3) Submit the next 5 outputs from that stream")
        print("4) Exit")
        choice = input("> ").strip()

        if choice == "1":
            if leak_revealed:
                print("Query phase is over.")
                continue
            if queries_left == 0:
                print("No queries left.")
                continue

            try:
                state = int(input("state: ").strip())
            except ValueError:
                print("Invalid input.")
                continue

            if state < 0 or state > MASK32:
                print("State must be in [0, 2^32 - 1].")
                continue

            print(f"T(state) = {xorshift32(state, a, b, c)}")
            queries_left -= 1
        elif choice == "2":
            if leak_revealed:
                print(f"x1 = {x1}")
                continue

            leak_revealed = True
            print("[info] The hidden update is linear over GF(2).")
            print("[info] Think about what happens on basis states.")
            print(f"x1 = {x1}")
        elif choice == "3":
            if not leak_revealed:
                print("Leak the stream output first.")
                continue
            submit_solution(expected_outputs)
            return
        elif choice == "4":
            print("Bye.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
