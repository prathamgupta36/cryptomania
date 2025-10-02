#!/usr/bin/exec-suid -- /usr/bin/python3
from helper import *
import secrets
from typing import List

def bytes_to_bitlist_big_endian(b: bytes) -> List[int]:
    out = []
    for byte in b:
        for i in range(8):
            out.append((byte >> (7 - i)) & 1)
    return out

n = 128

secret_bytes = secrets.token_bytes(16)
secret_bitlist = bytes_to_bitlist_big_endian(secret_bytes)

rng = create_random_seeded_generator(secrets.randbits(64))

superincreasing_sequence = generate_superincreasing_sequence(n, rng)

modulus_B = choose_modulus_B_greater_than_twice_last_r(superincreasing_sequence, rng)
multiplier_A = choose_multiplier_A_coprime_to_B(modulus_B, rng)

public_key_list = create_public_key_from_trapdoor(multiplier_A, modulus_B, superincreasing_sequence)

ciphertext_S = compute_ciphertext_from_public_key_and_message(public_key_list, secret_bitlist)

challenge_path = save_challenge_file(public_key_list, ciphertext_S, "challenge.txt")

print("Knapsack challenge")
print("Files written:")
print(" -", challenge_path)
print()
print("Submit the recovered secret as 32 hex characters (16 bytes).")

submission = input().strip()

if submission.lower() == secret_bytes.hex().lower():
	with open("/flag", "r") as f:
		print("Correct! Here is a flag for your troubles:\n")
		print(f.read())
else:
    print("Incorrect")

