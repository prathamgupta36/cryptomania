#!/usr/bin/exec-suid -- /usr/bin/python3
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time, random, sys
from Crypto.Util.number import getPrime, inverse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

console = Console()
console.print()

message = Text("friends don't let friends skip crypto", justify="center", style="dim")
panel = Panel.fit(
    message,
    title="[bold magenta]PwnPal[/]",
    subtitle="[red]v0.1 beta[/]",
    border_style="green"
)
console.print(panel)
console.print()

def chat_print(name, message, color, cps=60):
    console.print(f"[bold {color}]{name}[/]: ", end="")
    base_delay = 1.0 / cps
    for ch in message: 
        console.print(ch, end="", soft_wrap=True)
        #sys.stdout.flush()
        time.sleep(base_delay * random.uniform(0.5, 1.2))
    console.print()

chat_print("Alicia", "hey can you send me that flag?", "red")
chat_print("Bobert", "sure, but lets do it over a secure channel, what are your RSA credentials?", "magenta")
chat_print("Alicia", "here you go: ", "red")

p = getPrime(1024)
q = getPrime(1024)
N = p * q
phi = (p - 1) * (q - 1)
e = 0x10001
d = inverse(e, phi)

chat_print("Alicia", f"N: {hex(N)}\n\te: {hex(e)}", "red", 5000)
chat_print("Bobert", "sweet, here's the AES key:", "magenta")

FACTOR_BITS = 20
R = 1 << FACTOR_BITS

x = random.randrange(2, R)
y = random.randrange(2, R)
m = x * y

AES_KEY = int.to_bytes(m, length=16, byteorder='little') 

c = pow(m, e, N)

chat_print("Bobert", f"key: {hex(c)}", "magenta", 5000)

iv = get_random_bytes(16)
cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
message = b"Sweet we should be safe from hackers now, there's no way they could possibly see this"
pad_len = 16 - (len(message) % 16)
padded = message + bytes([pad_len]) * pad_len
aes_ct = cipher.encrypt(padded)

iv_b64 = base64.b64encode(iv).decode()
ct_b64 = base64.b64encode(aes_ct).decode()

chat_print("Alicia", f"{iv_b64}{ct_b64}", "red", 5000)
time.sleep(0.6)

with open("/flag", "rb") as f:
   FLAG = f.read()

iv = get_random_bytes(16)
cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
message = b"Heres the flag: " + FLAG
pad_len = 16 - (len(message) % 16)
padded = message + bytes([pad_len]) * pad_len
aes_ct = cipher.encrypt(padded)

iv_b64 = base64.b64encode(iv).decode()
ct_b64 = base64.b64encode(aes_ct).decode()

chat_print("Bobert", f"{iv_b64}{ct_b64}", "magenta", 5000)
