#!/usr/bin/exec-suid -- /usr/bin/python3
from Crypto.Util.number import getPrime, bytes_to_long, inverse, long_to_bytes
from random import getrandbits 
from math import gcd
from rich.console import Console
from rich.panel import Panel
import random
import string

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

def view_data():
    try:
        inp = input('Please provide user key e, d (comma seperated): ')
        e_str, d_str = inp.split(',')
        e, d = int(e_str.strip()), int(d_str.strip())
    except ValueError:
        print('ERROR: please provide valid key values\n')
        return
    if (e, d) not in users:
        print('Invalid user credentials')
        return
    print('Welcome user!')
    print('User Data:')
    if not users[(e,d)]:
        print('No data.\n')
    else:
        for ct in users[(e, d)]:
            data = long_to_bytes(decrypt(d, ct)).decode()
            print(data, "\n")

def get_password(length):
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choices(chars, k=length))
    return password

e, d = create_account()

with open ("/flag", "r") as f:
    flag = f.read()

ct = encrypt(e, bytes_to_long(flag.encode()))
users[(e,d)].append(ct)

while True:
    print('Welcome, please choose an action:')
    print('1: Create Account')
    print('2: List Accounts')
    print('3: View data')
    print('4: Exit')
    try:
        action = int(input('\nChoice: '))
    except ValueError:
        print('ERROR: Please enter a valid number\n')
        continue

    if action == 1:
        e, d = create_account()
        print(f'Account created!\nN = {N}\ne = {e}\nd = {d}\n')
    elif action == 2:
        list_accounts()
    elif action == 3:
        view_data()
    elif action == 4:
        print('Goodbye!')
        exit()
    else:
        print('ERROR: Invalid choice\n')

