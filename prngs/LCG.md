# Linear Congruential Generators

Pseudo-random number generators are deterministic algorithms that produce sequences which look random, even though every output is completely determined by the internal state. One of the simplest and most important examples is the linear congruential generator, or LCG.

## The basic idea

An LCG keeps a single integer state `x_n` and updates it with a fixed arithmetic rule:

```text
x_(n+1) = (a * x_n + c) mod m
```

Here:

- `x_n` is the current state
- `a` is the multiplier
- `c` is the increment
- `m` is the modulus

Each time you apply the recurrence, you get a new state. That new state is then used as the next output, or as the source of the next output.

This is the core intuition behind using an LCG as a PRG:

1. Start from a seed.
2. Repeatedly apply a deterministic update rule.
3. Treat the resulting values as a random-looking sequence.

If you do not know the seed, the outputs can appear irregular. But the generator is not actually random. It is just following a mathematical rule.

## Why modular arithmetic is used

Without the `mod m`, the state would grow without bound. The modulus keeps the state inside a fixed range:

```text
0 <= x_n < m
```

This makes the generator efficient and easy to implement. It also means the generator has a finite state space, so eventually the sequence must repeat. A well-chosen LCG tries to make that repetition happen as late as possible.

## Park-Miller

The Park-Miller generator is a famous special case of an LCG. It is defined by:

```text
x_(n+1) = (16807 * x_n) mod (2^31 - 1)
```

So its constants are:

- `a = 16807`
- `c = 0`
- `m = 2147483647`

This is sometimes called the "minimal standard" generator. Historically, it was popular because it is easy to implement, fast, and mathematically clean.

Unlike the general LCG formula, Park-Miller uses no increment. The next state is produced only by multiplying the current state by a fixed constant and reducing modulo a large prime.

## Why it looks random

A good PRG does not need to be truly random. It only needs to produce outputs that are difficult to distinguish from random for the intended use.

For a simple generator like Park-Miller, the combination of multiplication and modular reduction causes the state to move around a large set of values in a way that can look noisy to a casual observer. Different seeds produce different sequences, and the period can be long enough for small applications.

That is why LCGs were historically used in simulations, games, and older libraries.
