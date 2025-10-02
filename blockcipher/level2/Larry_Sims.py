#!/usr/bin/exec-suid -- /usr/bin/python3

import os, binascii
import AES_implementation as aes_mod
import pyfiglet
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
    cts.append(aes_mod.encrypt(secret_padded[i:i+16], KEY, num_rounds=2))

stored_cipher_hex = (b"".join(cts)).hex().lower()

def _rowmajor_to_colmajor_bytes(block: bytes) -> bytes:
    if len(block) != 16:
        return block
    state = [list(block[i:i+4]) for i in range(0, 16, 4)]
    out = bytearray(16)
    for col in range(4):
        for row in range(4):
            out[col * 4 + row] = state[row][col]
    return bytes(out)

print(Fore.LIGHTYELLOW_EX + pyfiglet.figlet_format("MIKE TYSON'S PUNSH OUT", font="larry3d"))
while True:
    print(Fore.GREEN   + "1) Encrypt your phrase of choice (2-round AES)")
    print(Fore.CYAN    + "2) Show encrypted super secret phrase")
    print(Fore.YELLOW  + "3) Do you know the phrase?")
    print(Fore.MAGENTA + "4) Decrypt stored secret phrase (QOL update)")
    print(Fore.WHITE   + "5) Exit\n")

    choice = input("Select an option (1-5): ").strip()

    if choice == "1":
        pt = input("Phrase to encrypt: ").encode()
        rem = len(pt) % 16
        if rem != 0:
            padlen = 16 - rem
            pt += bytes([padlen]) * padlen

        cts = []
        for i in range(0, len(pt), 16):
            cts.append(aes_mod.encrypt(pt[i:i+16], KEY, num_rounds=2))

        all_ct = b"".join(cts)
        print("\nCiphertext (hex):", all_ct.hex(), "\n")

        for idx, ct in enumerate(cts):
            print(f"block {idx:02d}: {ct.hex()}")
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
            g_cts.append(aes_mod.encrypt(guess_padded[i:i+16], KEY, num_rounds=2))

        guess_hex = (b"".join(g_cts)).hex().lower()

        if guess_hex == stored_cipher_hex:
            with open(FLAG_PATH, "r") as f:
                print("\n" + f.read().strip() + "\n")
            break
        else:
            print("\nIncorrect phrase :(, might be time to go train your boxing skills.\n")

    elif choice == "4":
        key_hex = input("Enter AES key (hex): ").strip()
        try:
            key = bytes.fromhex(key_hex)
        except ValueError:
            print("\nERROR: key must be valid hex (32 chars for AES-128).\n")
            continue
        if len(key) != 16:
            print("\nERROR: key must be 16 bytes (32 hex chars).\n")
            continue

        ct_all = bytes.fromhex(stored_cipher_hex)
        plaintext_blocks = []
        for i in range(0, len(ct_all), 16):
            block = ct_all[i:i+16]
            pt_block = aes_mod.decrypt(block, key, num_rounds=2)
            pt_block = _rowmajor_to_colmajor_bytes(pt_block)
            plaintext_blocks.append(pt_block)

        all_pt = b"".join(plaintext_blocks)
        padlen = all_pt[-1]
        if 1 <= padlen <= 16 and all_pt.endswith(bytes([padlen]) * padlen):
            all_pt = all_pt[:-padlen]

        try:
            print("Decrypted secret (utf-8):", all_pt.decode('utf-8'))
        except Exception:
            print("Decrypted secret could not be decoded as UTF-8.")
        print()

    elif choice == "5":
        print("\nCan't beat Iron Mike\n")
        break

    else:
        print("Invalid selection.")

