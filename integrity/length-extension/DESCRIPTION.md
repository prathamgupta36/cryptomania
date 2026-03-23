## Length Extension

This challenge focuses on the classic SHA-256 length extension attack against a naive hash-based construction. You are given the hash of an unknown 55-byte message and an attacker-controlled suffix.

Use the known message length to reconstruct the Merkle-Damgard padding and compute the digest of `secret || padding || suffix` without learning the original secret.
