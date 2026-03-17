#!/usr/bin/exec-suid -- /usr/bin/python3 -I
import sys

MOD31 = 2147483647  # 2^31 - 1

def glibc_random_sequence(seed, count):
    """
    Generate `count` outputs of glibc random() for a given seed.
    This follows the description in Peter Selinger's writeup.

    r[0] = seed
    r[1..30] = (16807 * r[i-1]) mod (2^31 - 1)
    r[31..33] = r[i-31]
    r[i] = (r[i-3] + r[i-31]) mod 2^32 for i >= 34
    random() output = (unsigned) r[i] >> 1, starting from i = 344
    """
    needed = 344 + count  # we need state up to index 343 + (count-1)
    r = [0] * needed
    r[0] = seed
    
    print(f"Seed table of {len(r)} elements: {r}")

    # Step (2): Park–Miller LCG seed expansion
    for i in range(1, 31):
        r[i] = (16807 * r[i - 1]) % MOD31
        # r[i] is always in [0, 2^31-2], so no need to adjust negatives here.
    
    print(f"Seed table of {len(r)} elements: {r}")

    initial_seed_table = r[:31]

    # Step (3): copy
    for i in range(31, 34):
        r[i] = r[i - 31]

    print(f"Seed table of {len(r)} elements: {r}")

    # Step (4): additive recurrence with 32-bit wrap-around
    for i in range(34, needed):
        r[i] = (r[i - 31] + r[i - 3]) & 0xFFFFFFFF

    # Step (5): outputs from index 344 onward; drop LSB
    out = []
    for i in range(344, 344 + count):
        out.append((r[i] & 0xFFFFFFFF) >> 1)
    return initial_seed_table, r

def print_seed_table(table):

    for i in range(344):
        print(f"Value at index {i}: {table[i]}")

    print("\nBREAK\n")

    for i in range(344, len(table)):
        print(f"Random values from LCG: {(table[i] & 0xFFFFFFFF) >> 1}")

def dump_table(table, filename):
    try: 
        with open(filename, "w") as fp:
            for val in table:
                fp.write(str(val) + "\n")

    except Exception as e:
        print(f"Error writing to file: {e}")

def get_super_secret_seed(filename):

    with open(filename, "r") as fp:
        seed = fp.read()
    return int(seed)

def main():
    seed = get_super_secret_seed("/challenge/super_secret_seed")
    initial_seed_table, full_table = glibc_random_sequence(seed, 5)
    dump_table(initial_seed_table, "/challenge/seed_table")
    dump_table(full_table[-5:], "/challenge/random")

if __name__ == "__main__":
    main()
