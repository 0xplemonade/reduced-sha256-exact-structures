# Exact two-bit carry transfer and reset

For the seven operands in the SHA-256 addition producing the next `a` word,
write

```text
beta_i = sigma_i + kappa_i - 2*kappa_(i+1).
```

`beta_i` is a signed bit difference and is therefore in `{-1,0,1}`.  Put
`q = sigma_i + kappa_i`.  If `q` is even, the right side shows that `beta_i`
is even.  Hence

```text
beta_i = 0,
kappa_(i+1) = q/2.
```

At the next bit, impose

```text
sigma_(i+1) = -q/2.
```

The aggregate totals are then equal, giving

```text
beta_(i+1) = 0,
kappa_(i+2) = 0.
```

This is a two-bit **carry-transfer-and-reset** characteristic.  It strictly
contains the earlier immediate-reset condition `q=0`: nonzero even `q` may
transfer a carry difference for one bit and cancel it at the next bit.

Once `kappa_(i+2)=0`, each subsequent `sigma_j=0` keeps both the output bit and
the next carry difference equal.  The matching bits of `B0` remain independent
reachable-state conditions and must be checked on complete fixed-IV chart
members.

The experiment instantiates `i=8`.  Its exact antecedent is:

```text
B0 = 0 mod 2^10
B1 = 0 mod 2^8
q = sigma_8 + kappa_8 is even
sigma_9 = -q/2
```

The conclusion is `B0=B1=0 mod 2^10` and `kappa_10=0`.  Adding
`B0=0 mod 2^11` and `sigma_10=0` extends the joint closure through bit ten.

