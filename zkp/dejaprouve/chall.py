#!/usr/bin/exec-suid -- /usr/bin/python3

from random import randint
from Crypto.Util.number import getPrime  # type: ignore

q = getPrime(512)
g = 2

transcript_log = {}


def _in_Zq_star(x):
    return 1 <= x < q


def main():
    print("\nFor this challenge, you will once again act as the prover (P).")
    print("The setup is the same as before: prove that you know x such that h = g^x mod q, without revealing x.")
    print("\nThis verifier was written by an intern who was very proud of an optimisation they made.")
    print("Something about it seems off. Can you figure out what they did wrong?")
    print("\nYou have 5 sessions to convince the verifier. A single accepted proof wins the flag.")
    print(f"\nPrime order (q): {q}")
    print(f"Generator  (g): {g}")

    x = randint(1, q - 1)
    h = pow(g, x, q)
    print(f"Public key (h): {h}\n")

    for session in range(1, 6):
        print(f"--- Session {session}/5 ---")

        u_raw = input("Provide your commitment (u) s.t. u = g^r mod q: ")
        try:
            u = int(u_raw)
        except ValueError:
            print("Invalid input.")
            continue
        if not _in_Zq_star(u):
            print(f"Invalid value: u={u} is not in Z_q*")
            continue

        if u in transcript_log:
            c = transcript_log[u]
        else:
            c = randint(0, q - 1)
            transcript_log[u] = c

        print(f"Challenge: {c}")

        z_raw = input("Provide your response (z) s.t. g^z ≡ u * h^c (mod q): ")
        try:
            z = int(z_raw)
        except ValueError:
            print("Invalid input.")
            continue
        if z % q == 0:
            print("Rejected: z == 0 mod q")
            continue

        if pow(g, z, q) == (u * pow(h, c, q)) % q:
            with open("/flag", "r") as f:
                print(f"Proof accepted! Here is your flag: {f.read()}")
            return
        else:
            print("Proof rejected.\n")

    print("Out of sessions.")


if __name__ == "__main__":
    main()
