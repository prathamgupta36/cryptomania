#!/usr/bin/exec-suid -- /usr/bin/python3

from random import randint 
from Crypto.Util.number import getPrime # type: ignore - stop Pylance from being stupid 


q = getPrime(512)
g = 2


def _in_Zq_star(x): 
    global q 
    return 1 <= x < q


def main() -> None: 
    print("Welcome to zero-knowledge proofs!")
    print("Zero-knowledge proofs (ZKPs) are an important cryptographic mechanism that enables one party (the prover) to prove to another party (the verifier) that a certain statement is true without revealing any information beyond the validity of the statement.")
    print("ZKPs are thus important in information-sensitive applications, such as blockchains. They provide a revolutionary form of zero trust, where authentication can be implemented without disclosing any information, such as key material.")
    print("\nFor this introductory challenge, let's practice ZKP interactions between prover and verifier!")
    print("Let's say the prover (P) wants to prove to the verifier (V) that they know the discrete logarithm (x) of some value [h = g^x mod q] without having to reveal the value of x.")
    print("The generator (g) generates a multiplicative group Zq of which x is a member, with the prerequesite that calculating the discrete logarithm for h = g^x mod q is difficult without the knowledge of x.")
    print("The Schnorr Identification Protocol provides a mechanism of interaction whereby this proof can be conducted between P and V with zero trust. You can review this protocol here: https://www.zkdocs.com/docs/zkdocs/zero-knowledge-protocols/schnorr/#schnorrs-identification-protocol")
    print("In practice, this protocol typically uses values within a subgroup of q, but for simplicity, we will continue forward with q")
    print("For this challenge, you will act as the prover (P). Convince the server that you know the value of x through Schnorr's protocol, without ever giving up x!")
    print("You will be provided with the prime order (q) and the generator (g). Use it to provide a message h s.t. h = g^x mod q, created with an x in the group Z_q, and your prover statement (u) s.t. u = g^r, with r in Z_q*")
    print(f"\nValue of prime order (q): {q}\nValue of generator (g): {g}")

    # Schnorr validation 
    h = input("Provide your message (h) s.t. h = g^x mod q: ")
    u = input("Provide your proving statement (u) s.t. u = g^r and r is in Z_q*: ")
    try: 
        h = int(h) 
        u = int(u)
    except ValueError: 
        print("Invalid input: the values should be integers")
        return 
    if not _in_Zq_star(h): 
        print(f"Invalid value: The value of h {h} is not in the multiplicative group Z_q*")
        return 
    elif not _in_Zq_star(u): 
        print(f"Invalid value: The value of u {u} is not in the multiplicative group Z_q*")
        return 
    
    c = randint(0, q-1)
    print(f"Okay, your message and initial statement were valid. Here is your challenge: {c}\n")
    print("Prove your knowledge of x by providing a z s.t. [z = r + x * c]")

    z = input("Provide your z: ")
    try: 
        z = int(z)
    except ValueError: 
        print("Invalid input: the values should be integers")
        return 
    if z == 0 % q: 
        print("Invalid value: your proof failed - z == 0 mod q")
        return 
    if pow(g, z, q) == (u*pow(h, c, q)) % q: 
        with open("flag", "r") as f: 
            print(f"Congratulations on your proof! You convinced me that you know such an x. Here is your flag: {f.read()}")
            return 
    else: 
        print("Invalid value: your proof failed - g^z != u * h^c")
        return  


if __name__ == "__main__": 
    main() 
