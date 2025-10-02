#!/usr/bin/exec-suid -- /usr/bin/python3
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from hidden_code import check_poly
import os

p = getPrime(512)
q = getPrime(512)
n = p*q
e = 3
secret = os.urandom(8).hex()
msg = 'Session Cookie: {user: "admin", secret: "' + secret + '"}'
m = bytes_to_long(msg.encode())
c = pow(m, e, n)

intro = '''
Welcome to the first coppersmith training challenge!

In this challenge you will practice your polynomial crafting skills by creating a polynomial
that will eventually allow you to decrypt the admins secret. You will be provided with an rsa
pubkey (n, e) and a ciphertext c. By viewing this challenges code you may notice that the encrypted
message has a format. It is you task to correctly interpret this extra info and distill your
knowledge into a modular polynomial that when coppersmiths method is applied will allow you to
decrypt the full ciphertext. Your answer will be the list of coefficients in your polynomial with
the lowest degree term first. For example, if f(x) = x^3 + 5x + 4, my answer would be "4,5,0,3".
You will then be prompted for the modulus for the polynomial.

NOTE: DO NOT reduce the coefficients of the polynomial by the desired modulus or the check will fail
'''

print(intro)
print(f"n={n}")
print(f"e={e}")
print(f"c={c}\n")

raw_vec = input("Provide the coefficient vector for you polynomial as a comma seperated list of integers: ")
poly = [int(x.strip()) for x in raw_vec.split(',')]
mod = int(input("Provide the modulus of your polynomial: "))

if check_poly(n, c, poly, mod):
    print("\nGood Job!")
    print(open('/flag', 'r').read())
else:
    print("You failed, better luck next time!")


