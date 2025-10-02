#!/usr/bin/env python3
from Crypto.Util.number import getPrime, bytes_to_long
from math import gcd
from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel.fit("🔒 Finally secure 🔒", title="RSA Vault", style="bold cyan"))
print()

e = 3

accounts = []  

def gen_modulus(bits=1024):
    while True:
        p = getPrime(bits)
        q = getPrime(bits)
        N = p * q
        phi = (p - 1) * (q - 1)
        if gcd(e, phi) == 1:
            return N

def encrypt(N, m):
    return pow(m, e, N)

def list_accounts():
    if not accounts:
        print("No accounts yet.\n")
        return
    print("accounts:")
    for i, a in enumerate(accounts, 1):
        print(f"{i}. N = {a['N']}")
        print(f"   e = {e}")
        print(f"   c = {a['ct']}\n")

def create_recipient(M):
    N = gen_modulus()
    c = encrypt(N, M)
    accounts.append({"N": N, "ct": c})

with open("/challenge/company_password.txt", "r") as m:
    m = m.read().strip()
M = bytes_to_long(m.encode())

for _ in range(e):
    create_recipient(M)

while True:
    print("Welcome, please choose an action:")
    print("1: List accounts (N, e, c)")
    print("2: Create another account")
    print("3: Exit")
    try:
        action = int(input("\nChoice: "))
    except ValueError:
        print("ERROR: Please enter a valid number\n")
        continue

    match action:
        case 1:
            list_accounts()
        case 2:
            m = input("please provide a message: ")
            m = bytes_to_long(m.encode())
            create_recipient(m)
        case 3:
            print("Goodbye!")
            exit()
        case _:
            print("ERROR: Invalid choice\n")

