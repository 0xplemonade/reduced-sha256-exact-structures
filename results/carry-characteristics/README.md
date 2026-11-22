# Carry-transfer and carry-reset characteristics

**Evidence class:** proved local carry identity with six constructive witnesses.

For one bit of the seven-operand SHA-256 round sum, let `sigma` be the signed
operand-bit difference and `kappa` the incoming carry difference. The output
bit difference satisfies `beta = sigma + kappa - 2*kappa_next`. When
`sigma + kappa` is even, the output bit closes and the carry difference becomes
half that sum.

Six complete 40-word schedule pairs exhibit a two-bit transfer and reset inside
the declared r40 families. The verifier reconstructs both schedules, replays
both compression traces from the standard IV, and checks every saved carry.

These local characteristics are not full boundary roots, collisions, or attack
cost improvements.
