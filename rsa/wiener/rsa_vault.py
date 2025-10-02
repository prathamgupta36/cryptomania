#!/usr/bin/exec-suid -- /usr/bin/python3
from Crypto.Util.number import getPrime, bytes_to_long, inverse, long_to_bytes
import math
import random
from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel.fit("🔒 Secure Login 🔒", title="RSA Vault", style="bold cyan"))
print()


p = getPrime(1024)
q = getPrime(1024)
N = p * q
phi = (p - 1) * (q - 1)

d_bound = math.isqrt(math.isqrt(N)) // 3

# my decryption too slow *angry face* i'll make it quick
while True:
    d = random.randrange(2, max(3, d_bound))  
    if math.gcd(d, phi) == 1:
        try:
            e = inverse(d, phi)  
        except ValueError:
            continue
        
        if 1 < e < phi:
            break

print(d)
data = []

def encrypt(m_int: int) -> int:
    return pow(m_int, e, N)

def decrypt(c_int: int) -> int:
    return pow(c_int, d, N)

def upload_data(m):
    try:
        m_int = bytes_to_long(m)
    except Exception as exc:
        print("Error converting bytes to integer:", exc)
        return
    c_int = encrypt(m_int)
    data.append(c_int)

def decrypt_data():
    try:
        d_input = input("Provide private exponent d: ").strip()
        d_val = int(d_input)
    except Exception:
        print("Invalid exponent")
        return
    try:
        m_int = pow(data[0], d_val, N)
        plaintext_bytes = long_to_bytes(m_int)
        try:
            print(plaintext_bytes.decode('utf-8'))
        except Exception:
            print(plaintext_bytes.hex())
    except:
        print('Error decrypting')

def list_data():
    print(f"N: {N}")
    print(f"e: {e}")
    for i, entry in enumerate(data):
        print(f"Data entry {i}: {entry}")

try:
    with open('/flag', 'rb') as f:
        flag = f.read().strip()
except:
    print('Error reading flag')
    exit()

upload_data(flag)

while True:
    print('Welcome, please choose an action:')
    print('1: Show Data')
    print('2: Decrypt data')
    print('3: Exit')
    try:
        action = int(input('\nChoice: '))
    except ValueError:
        print('ERROR: Please enter a valid number\n')
        continue

    if action == 1:
        list_data()
    elif action == 2:
        decrypt_data()
    elif action == 3:
        print('Goodbye!')
        exit()
    else:
        print('ERROR: Invalid choice\n')

