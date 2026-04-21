#!/usr/bin/exec-suid -- /usr/bin/python3
# scalar_mult_challenge.py
from helper import *
from random import randint

ROUNDS = 100

def gen_instance():
    while True:
        p = rand_prime(2000, 10000)
        a = randint(1, p - 1)
        b = randint(1, p - 1)
        curve = ECC(p, a, b)
        if nonsingular(curve):
            break

    while True:
        x = randint(0, p - 1)
        rhs = (x * x * x + curve.a * x + curve.b) % p
        y = sqrt_mod_p(rhs, p)
        if y is None:
            continue
        P = Point(curve, x, y)
        if P.y % p != 0:
            break

    k = randint(20, 200)
    R = scalar_mul(curve, P, k)
    return curve, P, k, R

def main():
    print("The next important thing you must know for ECC is scalar multiplication.")
    print("Prove yourself by solving 100 scalar problems in a row! (pwntools is probably smart here)")
    print("We are working with a curve of the form: y^2 = x^3 + ax + b (mod p)")

    for i in range(1, ROUNDS + 1):
        curve, P, k, R = gen_instance()

        print(f"round={i}")
        print(f"p={curve.p}")
        print(f"a={curve.a}")
        print(f"b={curve.b}")
        print(f"P=({P.x},{P.y})")
        print(f"k={k}")
        print("Compute R = kP and input the resulting point as x,y or INF")
        s = input("R=").strip()

        if s.upper() in {"INF", "INFINITY", "O"}:
            if not R.inf:
                print("Incorrect.")
                return
        else:
            try:
                xs, ys = s.split(",")
                ux = int(xs.strip()) % curve.p
                uy = int(ys.strip()) % curve.p
            except Exception:
                print("Bad format.")
                return

            if R.inf or ux != R.x or uy != R.y:
                print("Incorrect.")
                return

        print("OK")

    print("All rounds complete!")
    with open("/flag", "r") as f:
        print(f.read())

if __name__ == "__main__":
    main()
