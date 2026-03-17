This is the first Xorshift challenge.

The oracle leaks one full output from a known `xorshift32` update:

```text
x ^= x << 13
x ^= x >> 17
x ^= x << 5
```

Your job is to recover the original seed `s0` and then predict the next 5 outputs to get the flag.
