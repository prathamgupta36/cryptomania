#!/usr/bin/exec-suid -- /usr/bin/python3 -I
import secrets
import subprocess

MASK32 = 0xFFFFFFFF
MASK64 = 0xFFFFFFFFFFFFFFFF
QUERY_BUDGET = 32
STREAM_COUNT = 8


def xorshift32(state, a, b, c):
    state ^= (state << a) & MASK32
    state ^= (state >> b) & MASK32
    state ^= (state << c) & MASK32
    return state & MASK32


def xorshift64(state, a=12, b=25, c=27):
    state ^= (state >> a)
    state ^= (state << b) & MASK64
    state ^= (state >> c)
    return state & MASK64


def xorshift64star(state, multiplier):
    state = xorshift64(state)
    output = (state * multiplier) & MASK64
    return state, output


def derive_outputs(seed, a, b, c, count):
    outputs = []
    cur = seed
    for _ in range(count):
        cur = xorshift32(cur, a, b, c)
        outputs.append(cur)
    return outputs


def derive_multiplier(outputs):
    multiplier = 0
    for i, value in enumerate(outputs):
        multiplier |= (value & 0xFF) << (8 * i)
    return multiplier | 1


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


def submit_solution(expected_output):
    try:
        guess = int(input("Next xorshift64* output: ").strip())
    except ValueError:
        print("Try again.")
        return False

    if guess != expected_output:
        print("Try again.")
        return False

    print("All correct. Printing flag:")
    print_flag()
    return True


def main():
    seed = choose_seed()
    a, b, c = choose_params()

    stream = derive_outputs(seed, a, b, c, STREAM_COUNT)
    x1 = stream[0]
    multiplier = derive_multiplier(stream)
    state64 = ((stream[6] & MASK32) << 32) | (stream[7] & MASK32)
    _, expected_output = xorshift64star(state64, multiplier)
    queries_left = QUERY_BUDGET
    leak_revealed = False

    while True:
        print("\n=== Oracle Menu ===")
        print(f"1) Query the hidden one-step transition ({queries_left} queries left)")
        print("2) End query phase and leak one output from the secret stream")
        print("3) Submit the next xorshift64* output")
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
            print("[info] The hidden 32-bit update is linear over GF(2).")
            print("[info] Recover x2..x8 from x1 using the chosen-state oracle.")
            print("[info] Build the 64-bit multiplier with:")
            print("       m = sum(((xi & 0xFF) << (8 * (i - 1))) for i in 1..8)")
            print("       m |= 1")
            print("[info] Build the xorshift64* state with:")
            print("       state64 = (x7 << 32) | x8")
            print("[info] Public xorshift64* update:")
            print("       s ^= s >> 12; s ^= s << 25; s ^= s >> 27")
            print("       output = (s * m) mod 2^64")
            print(f"x1 = {x1}")
        elif choice == "3":
            if not leak_revealed:
                print("Leak the stream output first.")
                continue
            submit_solution(expected_output)
            return
        elif choice == "4":
            print("Bye.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
