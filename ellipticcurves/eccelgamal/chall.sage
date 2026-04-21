#!/usr/bin/exec-suid -- /usr/bin/sage

from helper import * 

# Setup secp256k1 curve 
F = FiniteField(2**256-2**32-2**9 -2**8 - 2**7 - 2**6 - 2**4 - 1)
E = EllipticCurve(F, [0, 7])
# Generator/base point 
G = E(55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)
n  = 115792089237316195423570985008687907852837564279074904382605163141518161494337
na = getrandbits(256)
Qa = na * G 

message = generateMessage(16)

print("Now we will learn about elliptic curves specifically in cryptosystems. Let's use the ElGamal cryptosystem built on ECC.")
print("Before starting, if you want to learn more about this subtopic, you can consult section 5.4 of the textbook found here: https://github.com/amilajack/reading/blob/master/Cryptography/An%20Introduction%20to%20Mathematical%20Cryptography.pdf")
print("One of the challenges with ElGamal ECC is mapping the message onto the elliptic curve. For the purposes of this challenge" \
      "we will use the base point G to map the message integer onto the curve.")
print("This does mean that the goal is to recover the original point on the curve upon decryption rather than the original plaintext message. " \
      "Recovering the original message in this method involves solving the ECDLP, which we will cover later.\n")
print("First, we will work on encryption.")
print("You will be provided with Alice's public key, the base point, the order of the curve, and the message to encrypt.")
print(f"Curve: y^2 = x^3 + 7 (the secp256k1 curve)\nPublic key: {Qa}\nBase point: {G}\nOrder: {n}\nMessage: {message}\n")
print("Note that the message should be converted to hex and then to int for operations.")
print("Encrypt the message using the public key and provide the coordinates of the encrypted point.")

int_message = messageToInt(message)
s_real = int_message * G
try: 
      user_c1 = input("Provide your first coordinate C1 as two comma-separated integers, like c11, c12: ")
      c11, c12 = user_c1.strip(" ").split(",")
      user_c2 = input("Provide your second coordinate C2 as two comma-separated integers, like c21, c22: ")
      c21, c22 = user_c2.strip(" ").split(",")
      user_decrypted = decrypt(E(c11, c12), E(c21, c22), na)
      assert user_decrypted == s_real, "Sorry, those coordinates were incorrectly encrypted. Try again with new parameters!"
      print("Success! Way to go! Now let's try doing some decryption...\n")
except ValueError: 
    print("Sorry, your coordinates were not valid. Please ensure that you provide two comma-separated integers.")
    exit() 
except TypeError: 
    print("Sorry, your coordinates were not valid. Please ensure that you provide two comma-separated integers.")
    exit() 

print("For decryption, this time we will provide an encrypted message's coordinates and you will have to input the decrypted, original point on the EC." \
      " For simplicity, we will also provide the private key. The point is just to check your understanding of the decryption process.")
print("All the other parameters (the public key, the curve, etc.) aside from the message will be the same as before.")
print("Let's see if you have a true grasp on the elliptic curve implementation of ElGamal!")

message2 = generateMessage(16) 
int_message2 = messageToInt(message2)
s_real2 = int_message2 * G
enc1, enc2 = encrypt(int_message2, Qa, G)

print(f"Here is the private key: {na}")
print(f"Here are the encrypted points:\nC1: {enc1}\nC2: {enc2}")

try: 
      user_c = input("Provide your decrypted coordinate C as two comma-separated integers, like c1, c2: ")
      c1, c2 = user_c.strip(" ").split(",")
      assert s_real2 == E(c1, c2), "Sorry, those coordinates were not of the original point. Try again with new parameters!"
      print("Success! Congrats on becoming an ElGamal master! Here is your flag:\n")
      with open("/flag", "r") as f: 
           print(f.read())
except ValueError: 
    print("Sorry, your coordinates were not valid. Please ensure that you provide two comma-separated integers.")
    exit()   
except TypeError: 
    print("Sorry, your coordinates were not valid. Please ensure that you provide two comma-separated integers.")
    exit()    
