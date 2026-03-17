## leaky-lcg1

This challenge series introduces the idea that leaking internal PRNG state can completely break future outputs. The target generator is `glibc random()`, whose state begins with a seed table derived from a Park-Miller style recurrence.

The oracle lets you query a value from the seed table by index and then asks you to submit 5 consecutive outputs from the generator. Use the menu to get the leak and then provide the requested outputs when you are ready.
