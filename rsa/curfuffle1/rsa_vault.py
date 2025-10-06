#!/usr/bin/exec-suid -- /usr/bin/python3
from Crypto.Util.number import getPrime, bytes_to_long, inverse 
from random import getrandbits 
from math import gcd
from rich.console import Console
from rich.panel import Panel
console = Console()

console = Console()
console.print(Panel.fit("🔒 Secure Login 🔒", title="RSA Vault", style="bold cyan"))
print()

p = getPrime(1024)
q = getPrime(1024)
N = p * q
phi = (p - 1) * (q - 1)

users = {}

def encrypt(e, m):
    return pow(m, e, N)

def decrypt(d, c):
    return pow(c, d, N)

def create_account():
    while True:
        e = getrandbits(16)
        if gcd(e, phi) == 1:
            d = inverse(e, phi)
        else:
            continue
        if (e, d) in users:
            continue
        else:
            break
    users[(e, d)] = []
    return e, d

def list_accounts():
    print('Accounts: ')
    for (e, _), data in users.items():
        print(f"\te = {e}, ct(s):")
        if not data:
            print(f"\t\tno data :(")
            continue
        for ct in data:
            print(f"\t\tciphertext = {ct}")
    print()


with open('/challenge/company_password.txt', 'r') as f:
    company_password = f.read().strip()

e, d = create_account()
ct = encrypt(e, bytes_to_long(company_password.encode()))
users[(e,d)].append(ct)

e, d = create_account()
ct = encrypt(e, bytes_to_long(company_password.encode()))
users[(e,d)].append(ct)

while True:
    print('Welcome, please choose an action:')
    print('1: Create Account')
    print('2: List Accounts')
    print('3: Exit')
    try:
        action = int(input('\nChoice: '))
    except ValueError:
        print('ERROR: Please enter a valid number\n')
        continue

    if action == 1:
        e, _ = create_account()
        print(f'Account created! N = {N}, e = {e}\n')
    elif action == 2:
        list_accounts()
    elif action == 3:
        print('Goodbye!')
        exit()
    else:
        print('ERROR: Invalid choice\n')
