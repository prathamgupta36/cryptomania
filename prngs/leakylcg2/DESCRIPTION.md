## leaky-lcg2

This challenge builds on the first level by leaking only one value from the initial seed table while hiding which table index it came from. Think about how even an unknown leak from structured PRNG state can still be enough to recover the generator and predict future values.

The oracle has one option to reveal the hidden-index table value and another option to submit the recovered seed together with the first 5 outputs of `glibc random()`.
