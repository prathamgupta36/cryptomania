#!/usr/bin/exec-suid -- /usr/bin/python3
import random
from math import gcd

from Crypto.Util.number import getPrime, inverse

p = getPrime(1024)
q = getPrime(1024)
N = p * q
phi_n = (p - 1) * (q - 1)
e = 65537
d = inverse(e, phi_n)


def _sign(message: int) -> int:
    return pow(message, d, N)


def main() -> None:
    with open("/flag", "r") as f:
        flag = f.read()

    while True:
        M = random.getrandbits(32)
        if gcd(M, N) == 1:
            break

    S_real = _sign(M)

    print(
        f"Bob might not be famous, but you would really like his signature on this message: {M}"
    )
    print(f"Here is Bob's public key <e, N>: <{e}, {N}>")
    print(
        "Bob is at least savvy enough to not sign this message but might be willing to provide his...autograph on another, random message"
    )

    try:
        M_prime = int(
            input("Provide an integer message and Bob will sign it: ").strip()
        )
    except ValueError:
        print("ERROR: Please enter a valid integer message next time.")
        exit(1)
    while M_prime == M:
        try:
            M_prime = int(
                input("Can't fool Bob - please provide a different message: ").strip()
            )
        except ValueError:
            print("ERROR: Please enter a valid integer message next time.")
            exit(1)

    S_prime = _sign(M_prime)

    print(f"Here is the signed message from Bob: {S_prime}")
    while True:
        try:
            S_candidate = int(
                input(
                    f"Let's see if you tricked Bob - provide his signature for the original message {M}: "
                ).strip()
            )
        except ValueError:
            print("ERROR: The signature should be an integer. Try again.")
        if S_candidate == S_real:
            print("Well done!")
            print(f"Here is your flag: {flag}")
            break
        else:
            print(
                f"Incorrect - this is not Bob's signature for {M}. Try again or exit and have Bob sign something else!"
            )


if __name__ == "__main__":
    main()
