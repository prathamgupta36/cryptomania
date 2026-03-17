## lockpick-lcg2

This challenge follows the same theme but this time the modulus is hidden as well. The core concept is that even when the modulus is not given, consecutive outputs from a linear congruential generator can still reveal the full recurrence.

The oracle leaks 10 consecutive outputs from the generator. Your task is to recover the modulus `m`, the multiplier `a`, the increment `c`, and then submit the next 5 outputs.
