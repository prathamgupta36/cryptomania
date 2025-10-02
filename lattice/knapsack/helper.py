#!/usr/bin/env python3
import random
from math import gcd

def create_random_seeded_generator(seed_value):
    random.seed(seed_value)
    return random

def generate_superincreasing_sequence(length_of_sequence, random_generator):
    sequence = []
    running_sum = 0
    for _ in range(length_of_sequence):
        base_next = running_sum * 2 + 1
        random_offset = random_generator.randint(0, max(1, running_sum // 4 + 1))
        next_value = base_next + random_offset
        sequence.append(next_value)
        running_sum += next_value
    return sequence

def choose_modulus_B_greater_than_twice_last_r(superincreasing_sequence, random_generator):
    last_r = superincreasing_sequence[-1]
    minimum_B = 2 * last_r + 1
    extra_factor = random_generator.randint(1, 4)
    return minimum_B * (1 + extra_factor)

def choose_multiplier_A_coprime_to_B(modulus_B, random_generator):
    while True:
        candidate_A = random_generator.randint(2, modulus_B - 1)
        if gcd(candidate_A, modulus_B) == 1:
            return candidate_A

def create_public_key_from_trapdoor(multiplier_A, modulus_B, superincreasing_sequence):
    return [(multiplier_A * r_value) % modulus_B for r_value in superincreasing_sequence]

def sample_random_binary_message(number_of_bits, random_generator):
    return [random_generator.randint(0, 1) for _ in range(number_of_bits)]

def compute_ciphertext_from_public_key_and_message(public_key_list, binary_message):
    return sum(bit * m for bit, m in zip(binary_message, public_key_list))

def save_challenge_file(public_key_list, ciphertext_integer, filename="challenge.txt"):
    with open(filename, "w") as f:
        f.write("n = " + str(len(public_key_list)) + "\n")
        f.write("public_key = " + str(public_key_list) + "\n")
        f.write("ciphertext = " + str(ciphertext_integer) + "\n")
    return filename

