#!/usr/bin/exec-suid -- /usr/bin/python3
from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel.fit("🔒 Super Secure 🔒", title="Some company", style="bold cyan"))
print()

with open("./company_password.txt","r") as f:
    company_password = f.read().strip()

pw = input("password: ").strip()

if pw == company_password:
    with open("/flag","r") as f:
        print(f.read().strip())
else:
    print("invalid")

