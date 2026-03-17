# Xorshift PRGs

## What is a Xorshift generator?

The **Xorshift** family is a class of pseudorandom number generators introduced
by George Marsaglia. These generators update their internal state using only:

- XOR
- bit shifts
- sometimes rotations
- sometimes a simple output scrambler such as multiplication or addition

They are popular because they are:

- very fast
- easy to implement
- small enough to study by hand

## The core idea

A basic Xorshift generator keeps some internal state `x` and repeatedly applies
a small sequence of XOR-and-shift operations.

For example, a 32-bit Xorshift might look like:

```c
uint32_t xs32(uint32_t x) {
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    return x;
}
```

The output is often just the updated state itself.

Even though this looks nonlinear at first glance, it is built entirely from
operations that are linear over the bits of the state.

## The basic variants

### Xorshift

This is the simplest form.

The state is updated by a few XOR and shift operations, and the new state is
returned as output.

Example:

```text
x ^= x << a
x ^= x >> b
x ^= x << c
```

This version is extremely instructive because the state transition can often be
recovered or inverted directly.

### Xorshift*

This variant applies a multiplication after the Xorshift update.

Example:

```text
x = xorshift64(x)
output = x * m mod 2^64
```

Here `m` is usually an odd constant.

The multiplication is meant to improve the quality of the output, but it does
not make the generator cryptographically secure. In many settings it can be
undone or incorporated into an attack.

### Xorshift+

This variant usually has a larger state and returns the sum of two state words.

Example idea:

```text
update the internal state
output = s0 + s1 mod 2^64
```

The `+` scrambler makes the output less obviously linear, but the generator is
still not suitable for cryptographic use.

### xoroshiro and xoshiro

These are later descendants of the Xorshift family.

They use:

- XOR
- rotations
- shifts
- small output scramblers such as `+`, `++`, or `**`

These generators are generally better designed for simulation and general
non-cryptographic use, but they are still **not cryptographic PRGs**.

## Why Xorshift is weak against attackers

The key weakness is structure.

For plain Xorshift generators:

- the state transition is linear over `GF(2)`
- each bit of output is a predictable combination of input bits
- enough output often lets you reconstruct the entire internal state

For scrambled variants like `*` and `+`:

- the scrambler may hide the structure a bit
- but the core engine is still highly structured
- if the scrambler is reversible or partially leaked, the state may still be
  recoverable

## Xorshift vs cryptographic PRGs

A cryptographic PRG should make it computationally infeasible to predict future
outputs or recover past state from observed output.

Xorshift generators do not provide that guarantee.

They are usually designed for:

- speed
- simplicity
- statistical quality in non-adversarial settings

They are **not** designed to resist:

- state recovery
- output prediction
- chosen-input or chosen-state attacks
- side-channel style leakage

## Why we use them in these challenges

In these challenges, Xorshift generators are not the final goal. They are just the
means for learning.

By the end of this module you should come away understanding:

1. How to reason about bitwise state updates.
2. Why XOR-and-shift recurrences can often be inverted.
3. How linear algebra over bits can recover a hidden transition.
4. Why output scrambling does not automatically imply security.
5. Why "fast PRNG" and "secure PRG" are very different goals.

## Summary

The Xorshift family is a great introduction to PRG attacks because it exposes
the difference between:

- generating numbers that "look random"
- generating numbers that remain secure against an attacker

These generators are fast, elegant, and useful for learning, but they are not
safe as cryptographic random number generators.
