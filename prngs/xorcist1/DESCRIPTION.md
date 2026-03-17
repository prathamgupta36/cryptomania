# xor-cist1

This challenge introduces a chosen-state oracle.

The oracle hides a 32-bit Xorshift transition with secret shift parameters
`a`, `b`, and `c`, but it lets you query the one-step map `T(x)` on states of
your choice before it leaks one stream value `x1`.

To get the flag you need to predict the next 5 outputs from that stream.

## Interacting with the Oracle 

- Option `1`: query the hidden transition on a state you choose
- Option `2`: end the query phase and reveal `x1`
- Option `3`: submit the next 5 outputs

Important:

- You only get 32 chosen-state queries.
- After the leak, the query phase is over.
