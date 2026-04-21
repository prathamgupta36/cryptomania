#!/usr/bin/env sage
from sage.all import *
import hashlib
import secrets
import textwrap

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

F = GF(p)
E = EllipticCurve(F, [0, 7])

G = E(
    55066263022277343669578718895168534326250603453777594175500187360389116729240,
    32670510020758816978083085130507043184471273380659243275938904335757337482424
)

def H(msg: str) -> Integer:
    digest = hashlib.sha256(msg.encode("utf-8")).digest()
    return Integer(int.from_bytes(digest, "big")) % n

def deterministic_k(d: Integer, salt_hex: str, msg: str) -> Integer:
    """
    Deterministic nonce:
      k = (SHA256( d||salt||msg ) mod (n-1)) + 1

    d encoded as 32-byte big-endian.
    salt is 16 bytes (printed as hex).
    msg is UTF-8.
    """
    salt = bytes.fromhex(salt_hex)
    d_bytes = int(d).to_bytes(32, "big")
    data = d_bytes + salt + msg.encode("utf-8")
    digest = hashlib.sha256(data).digest()
    return Integer(int.from_bytes(digest, "big") % (n - 1) + 1)

def verify(msg: str, r: Integer, s: Integer, Q) -> bool:
    if not (1 <= r < n and 1 <= s <= (n // 2)):
        return False

    try:
        Q = E(Q[0], Q[1])
    except Exception:
        return False

    z = H(msg)
    w = inverse_mod(s, n)

    u1 = (z * w) % n
    u2 = (r * w) % n

    P = u1 * G + u2 * Q
    if P == E(0):
        return False

    return (Integer(P[0]) % n) == r

banner = """
ECC Signing Intro (ECDSA-style)

You must:
  1) Pick a private key d
  2) Compute Q = dG
  3) Compute deterministic k from d, salt, and message
  4) Produce a valid signature (r, s)

Definitions:
  z = SHA256(message) mod n
  k = (SHA256(d || salt || message) mod (n-1)) + 1
  R = kG
  r = x(R) mod n
  s = k^{-1} (z + r*d) mod n

Rule:
  low-s required: s must be <= n//2
"""
print(textwrap.dedent(banner).strip(), "\n")

print("=== Curve / Group Parameters ===")
print("Curve: y^2 = x^3 + 7 over F_p (secp256k1)")
print(f"p:\n  dec: {p}\n  hex: {hex(p)}")
print(f"n:\n  dec: {n}\n  hex: {hex(n)}")
print("G:")
print(f"  x = {Integer(G[0])}")
print(f"  y = {Integer(G[1])}\n")

message = "Give me the flag"
salt_hex = secrets.token_bytes(16).hex()

print("=== Instance ===")
print(f"Message:\n  {message}")
print(f"Salt (16 bytes hex):\n  {salt_hex}")
print(f"z = SHA256(message) mod n:\n  {H(message)}")
print(f"Low-s bound: n//2 = {n//2}\n")

try:
    d = Integer(input("Create your private key d (integer): ").strip())
except Exception:
    print("Invalid integer.")
    raise SystemExit(1)

# Validity checks on d
if not (1 <= d < n):
    print("Invalid d: must satisfy 1 <= d < n.")
    raise SystemExit(1)

if d < (1 << 128):
    print("Invalid d for this challenge: choose a larger private key (>= 2^128).")
    raise SystemExit(1)

Q = d * G
print("\nDerived public key Q = d*G:")
print(f"  x = {Integer(Q[0])}")
print(f"  y = {Integer(Q[1])}\n")

print("Now compute your signature using the definitions above and submit:")
try:
    r = Integer(input("Provide r: ").strip())
    s = Integer(input("Provide s: ").strip())
except Exception:
    print("Invalid integer.")
    raise SystemExit(1)

if verify(message, r, s, Q):
    print("\nValid signature!")
    print(open("/flag", "r").read())
else:
    print("\nInvalid signature.")
