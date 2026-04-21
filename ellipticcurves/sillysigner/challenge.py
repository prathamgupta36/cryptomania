#!/usr/bin/exec-suid -- /usr/bin/python3
import os
import hashlib
from Crypto.Cipher import AES
from helper import *

P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
A = -3
GX = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
GY = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
G = (GX, GY)
N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

def sign(msg, priv_key, k):
    z = int(hashlib.sha256(msg).hexdigest(), 16)
    K = scalar_mul(G, k, P, A)
    r = K[0] % N
    s = (inv_mod(k, N) * (z + r * priv_key)) % N
    return (r, s)

def main():
    if not os.path.exists("/flag"):
        print("Error: flag file not found.")
        return
    flag = open("/flag", "rb").read().strip()

    d = int.from_bytes(os.urandom(32), 'big') % N
    
    fixed_k = int.from_bytes(os.urandom(32), 'big') % N
    
    msg1 = b"Identity Verification Case #1029"
    msg2 = b"Identity Verification Case #1030"
    
    r1, s1 = sign(msg1, d, fixed_k)
    r2, s2 = sign(msg2, d, fixed_k)
    
    aes_key = hashlib.sha256(str(d).encode()).digest()[:16]
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(flag)

    print(f"n = {hex(N)}")
    print(f"Msg1: {msg1.decode()}")
    print(f"Sig1: r={hex(r1)}, s={hex(s1)}")
    print(f"Msg2: {msg2.decode()}")
    print(f"Sig2: r={hex(r2)}, s={hex(s2)}")
    print("-" * 20)
    print(f"nonce = {cipher.nonce.hex()}")
    print(f"ct = {ct.hex()}")
    print(f"tag = {tag.hex()}")

if __name__ == "__main__":
    main()
