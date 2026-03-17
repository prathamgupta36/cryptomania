#!/usr/bin/exec-suid -- /usr/bin/python3 -I
import subprocess

def load_int_file(filename):
    with open(filename, "r") as fp:
        return [int(line.strip()) for line in fp if line.strip()]


def get_seed_table(filename):
    return load_int_file(filename)


def get_val_from_seed_table(seed_table, idx):
    if idx < 1 or idx >= len(seed_table):
        raise IndexError("index out of range")
    return seed_table[idx]


def check(guess, idx, expected_values):
    return guess == expected_values[idx]


def print_flag():
    try:
        result = subprocess.run(
            ["cat", "/flag"], capture_output=True, text=True, check=True
        )
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    except Exception:
        print("Flag file is missing or unreadable.")


def main():
    seed_table = get_seed_table("/challenge/seed_table")
    random_values = load_int_file("/challenge/random")

    while True:
        print("\n=== Oracle Menu ===")
        print("1) Access a value from seed table")
        print("2) Submit 5 consecutive outputs")
        print("3) Exit")
        choice = input("> ").strip()

        if choice == "1":
            try:
                idx = int(input("Index in seed table: ").strip())
                value = get_val_from_seed_table(seed_table, idx)
                print(f"seed_table[{idx}] = {value}")
            except ValueError:
                print("Invalid input: index must be an integer.")
            except IndexError:
                print(f"Invalid index: choose 0..{len(seed_table) - 1}.")
        elif choice == "2":
            for i in range(5):
                try:
                    guess = int(input(f"output[{i}]: ").strip())
                except ValueError:
                    print("Try again.")
                    return
                if not check(guess, i, random_values):
                    print("Try again.")
                    return

            print("All 5 correct. Printing flag:")
            print_flag()
            return
        elif choice == "3":
            print("Bye.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
