#!/usr/bin/exec-suid -- /usr/bin/python3
import os
import hashlib
from Crypto.Cipher import AES
from helper import *

P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
A_COEFF = -3
B_COEFF = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
GX = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
GY = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5

def kdf(shared_x: int) -> bytes:
    """Derives a 16-byte AES key from the shared secret's x-coordinate."""
    return hashlib.sha256(shared_x.to_bytes(32, 'big')).digest()[:16]

def main():
    print("--- Secure Elliptic Curve Key Exchange ---")
    print("So you think you know ECC? Perform a real handshake to get your flag.")
    print(f"p = {P}")
    print(f"a = {A_COEFF}")
    print(f"b = {B_COEFF}")
    print(f"G = ({GX}, {GY})")

    alice_priv = int.from_bytes(os.urandom(32), 'big') % P
    
    Alice_Pub = scalar_mul((GX, GY), alice_priv, P, A_COEFF)
    
    print(f"Alice_Pub = ({Alice_Pub[0]}, {Alice_Pub[1]})")

    try:
        user_input = input("\nEnter your public key B as 'x,y': ").strip()
        bx, by = map(int, user_input.split(","))
        
        if not is_on_curve(bx, by, P, A_COEFF, B_COEFF):
            print("Error: That point is not on the curve!")
            return

        if (bx, by) == Alice_Pub or (bx, by) == (GX, GY):
            print("Error: Trivial or reflected point detected. Use your own keypair!")
            return

        Shared_Secret = scalar_mul((bx, by), alice_priv, P, A_COEFF)
        key = kdf(Shared_Secret[0])
            
        flag = open("/flag", "rb").read().strip()
        
        cipher = AES.new(key, AES.MODE_GCM)
        ct, tag = cipher.encrypt_and_digest(flag)

        print("\nEncryption complete. Use the shared secret to decrypt:")
        print(f"nonce = {cipher.nonce.hex()}")
        print(f"ct = {ct.hex()}")
        print(f"tag = {tag.hex()}")

    except Exception as e:
        print(f"Invalid input or error: {e}")

if __name__ == "__main__":
    main()
