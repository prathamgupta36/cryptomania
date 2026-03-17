## lockpick-lcg1

This challenge starts a pure LCG series based on recovering generator parameters from observed outputs. The generator follows the affine recurrence `x_(n+1) = (a*x_n + c) mod m`, where the goal is to recover the public constants that define the stream.

The oracle reveals the modulus `m` and 3 consecutive outputs. It then asks you to submit the multiplier `a`, the increment `c`, and the next 5 outputs in the sequence.
