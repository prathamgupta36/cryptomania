# xor-cist2

This challenge builds directly on `xor-cist1`.

You still get a chosen-state oracle for a hidden 32-bit Xorshift transition,
and you still leak only one stream value `x1`. But now you must recover more
than just future outputs: you must also recover the original seed `s0` to get the flag.
