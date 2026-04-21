#!/usr/bin/exec-suid -- /usr/bin/python3

from helper import * 
from random import randint
from math import sqrt

def main(): 
    while True: 
        try: 
            ecc = ECC(Fraction(randint(-20, 20)), Fraction(randint(-20, 20)))
            if ecc.a == 0 or ecc.b == 0: 
                continue 
            p_x = randint(1, 20) 
            p_y = sqrt(p_x**3 + (ecc.a * p_x) + ecc.b)
            if p_y == 0: 
                continue 
            point_p = Point(ecc, Fraction(p_x).limit_denominator(100), Fraction(p_y).limit_denominator(100))

            q_x = randint(1, 20) 
            if q_x == p_x: 
                continue 
            q_y = sqrt(q_x**3 + (ecc.a * q_x) + ecc.b)
            point_q = Point(ecc, Fraction(q_x).limit_denominator(100), Fraction(q_y).limit_denominator(100))
            break

            # Following example from textbook: 
            # ecc = ECC(-15, 18) 
            # point_p = Point(ecc, 7, 16)
            # point_q = Point(ecc, 1, 2)
            # point_r = helper.Point(ecc, -23/9, -170/27)
        except Exception as e: 
            pass 

    print(f"We have the geometric elliptic curve (ECC) defined by the following Weierstrass equation: {ecc}")
    print(f"We also have two points that are on the curve: point P {point_p} and point Q {point_q}")
    print("Add these two points together on the elliptic curve and input the resulting point in the form (Rx', Ry')")
    print("If either of the resulting coordinates are fractions, input them in reduced form with a '/' to denote the fraction bar.")
    print("\nNOTE: for this introduction, we have chosen to provide a very simple elliptic curve. As such, some approximations are made with the provided " \
    "points. Please follow the addition algorithm and approximate your solution with a denominator limit of 100, if needed.")
    print("You may find the following Python function useful for these approximations: https://docs.python.org/3/library/fractions.html#fractions.Fraction.limit_denominator")
   
    while True: 
        user_soln = input("\nPlease provide the solution to the addition: ")
        try: 
            (user_soln_x, user_soln_y) = user_soln.split(",")
            (user_fraction_x, user_fraction_y) = Fraction(user_soln_x.strip().strip("()")), Fraction(user_soln_y.strip().strip("()"))
            if (user_fraction_x, user_fraction_y) == ecc_addition(ecc, point_p, point_q): 
                print("\nCorrect! Well done!")
                with open("/flag", "r") as flag: 
                    print(f"Here's your flag: {flag.read()}")
                break 
            else: 
                print("That's not it, or your answer might not have been fully reduced. Try again!")

        except Exception as e: 
            print("The input was not properly recognized, please check your formatting")
            print(f"Exception: {e}") 

if __name__ == "__main__": 
    main() 
