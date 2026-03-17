# xor-cist3

This challenge is a bridge from plain Xorshift to `xorshift*`.

The first stage is the same style as the earlier `xor-cist` challenges: a
chosen-state oracle hides a 32-bit Xorshift transition, and later leaks one
stream value `x1`.

But instead of asking for more 32-bit stream outputs directly, this challenge
uses the recovered 32-bit stream as a seed to build a public `xorshift64*` instance.

Finally, you need to submit the resulting 64-bit output from the `xorshift64*` to get the flag.
