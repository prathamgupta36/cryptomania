#!/usr/bin/exec-suid -- /usr/bin/python3

import os, binascii
import AES_implementation as aes_mod
import pyfiglet
import secrets
from colorama import Fore

KEY = os.urandom(16)
SECRET_PATH = "/challenge/super_secret_phrase_only_the_cool_kids_know"
FLAG_PATH = "/flag"


with open(SECRET_PATH, "rb") as f:
    secret = f.read().rstrip(b"\r\n")  

rem = len(secret) % 16
padlen = 16 - rem if rem != 0 else 16
secret_padded = secret + bytes([padlen]) * padlen

cts = []
for i in range(0, len(secret_padded), 16):
    cts.append(aes_mod.encrypt(secret_padded[i:i+16], KEY, num_rounds=1))

stored_cipher_hex = (b"".join(cts)).hex().lower()

print(Fore.LIGHTYELLOW_EX + pyfiglet.figlet_format("MIKE TYSON'S PUNSH OUT", font="larry3d"))
while True:
    print(Fore.GREEN + "1) Encrypt your phrase of choice (1-round AES)")
    print(Fore.CYAN  + "2) Show encrypted super secret phrase")
    print(Fore.YELLOW + "3) Do you know the phrase?")
    print(Fore.WHITE + "4) Exit\n")



    choice = input("Select an option (1-4): ").strip()

    if choice == "1":
        pt = bytes.fromhex(input("Phrase to encrypt: ").strip())
        rem = len(pt) % 16
        if rem != 0:
            padlen = 16 - rem
            pt += bytes([padlen]) * padlen

        cts = []
        for i in range(0, len(pt), 16):
            cts.append(aes_mod.encrypt(pt[i:i+16], KEY, num_rounds=1))

        all_ct = b"".join(cts)
        print("\nCiphertext (hex):", (all_ct).hex(), "\n")

        for idx, ct in enumerate(cts):
            print(f"block {idx:02d}: {(ct).hex()}")
        print()

    elif choice == "2":
        print("\nEncrypted super secret phrase (hex):\n\n", stored_cipher_hex, "\n")

    elif choice == "3":
        guess = input("Enter super secret phrase: ").encode().rstrip(b"\r\n")
        rem = len(guess) % 16
        padlen = 16 - rem if rem != 0 else 16
        guess_padded = guess + bytes([padlen]) * padlen

        g_cts = []
        for i in range(0, len(guess_padded), 16):
            g_cts.append(aes_mod.encrypt(guess_padded[i:i+16], KEY, num_rounds=1))

        guess_hex = (b"".join(g_cts)).hex().lower()

        if guess_hex == stored_cipher_hex:
            with open(FLAG_PATH, "r") as f:
                print("\n" + f.read().strip() + "\n")
            break
        else:
            print("\nIncorrect phrase :(, might be time to go train your boxing skills.\n")
    
    elif choice == "4":
        print("\nCan't beat Iron Mike\n")
        break

    else:
        print("Invalid selection.")

