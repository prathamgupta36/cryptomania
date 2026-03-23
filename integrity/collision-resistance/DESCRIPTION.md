## Collision Resistance

This challenge studies collision resistance under an intentionally short digest. You must find two different messages, each at least 32 bytes long, that collide under a 5-byte SHAKE256 output.

Because the digest is so small, a birthday-style search is enough to find a collision. Submit both messages as hexadecimal.
