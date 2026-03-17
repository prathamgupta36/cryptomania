## leaky-lcg3

This challenge continues the state-leak theme, but instead of exposing a single table entry it leaks the sum of two hidden entries from the initial seed table. The concept here is that linear relations between secret state values can still carry enough information to compromise the generator.

The oracle reveals one sum of the form `seed_table[i] + seed_table[j]`, with both indices hidden and distinct. After that, you must submit the recovered seed and the first 5 outputs of `glibc random()`.
