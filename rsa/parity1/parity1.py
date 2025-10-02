#!/usr/bin/exec-suid -- /usr/bin/python3
from Crypto.Util.number import getPrime
from secrets import randbelow

FLAG = open('/flag', 'r').read().strip()

# you know the drill
p, q = getPrime(1024), getPrime(1024)
N=p*q
e = 65537
d = pow(e, -1, (p-1)*(q-1))

supersecret = randbelow(N)
ciphertext = pow(supersecret, e, N)


print(f'e : {e} \n\n N : {N}\n\n ciphertext : {ciphertext}')

for _ in range(N.bit_length()):
    try:
        c = int(input("I'll decrypt anything for you :> "))
        if c == ciphertext:
            print('... except that')
            continue

        hint = pow(c, d, N) & 1
        print(f"here's your hint: {hint}")

    except:
        print('???')
        break


v = int(input('One chance is all you get... '))
if v == supersecret:
    print(FLAG)