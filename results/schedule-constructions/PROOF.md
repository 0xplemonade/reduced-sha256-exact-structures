# Three chosen left outputs and exact S13-preserving completion fibres

## Result and scope

The reachable-S6 and released-late-core charts combine into a more useful
state-oriented coordinate system. Fix the actual common entry C, the two
initial prefixes through W9, and an admissible absolute left U=W22. Then

    (left A10, left A11, left A12, V, Z)
       in (Z/(2^32))^3 x J14 x J23

is an exact chart of the same fixed-prefix-and-U slice. Here V=W14_left and
Z=W23_left; A_t means the new a output of round t, so A10=S11[a].

The three left outputs are arbitrary. After fixing them, every V,Z choice
preserves BOTH absolute states at S13. The left and right states need not
equal one another. The remaining number of distinct paired completions is:

| Numerical arm | Completions for every fixed output triple / S13 pair |
|---|---:|
| Shifted public r38, p=4 | 2^54 |
| Public r37, p=1 | N^2, where N=2^27+2^22+2^19 |

This changes coordinates and exposes a state-preserving fibre. It adds no
cardinality to the earlier 2^150 p4 slice or N^2*2^96 p1 slice. It proves no
late endpoint equality, collision probability, search cost, or independent
lane interface. The frozen A/B/C comparison is unaffected.

## 1. Fixed context and admitted late words

All arithmetic is modulo 2^32, with right-minus-left differences. The
numerical cores have

    dW6=a, dW7=b, dW8=c, dW9=d, dW14=p, dW22=e, dW23=-p.

For p4:

    (a,b,c,d,p,e)=(31de0240,fffffffc,0,00028000,4,07ff0000).

For p1:

    (a,b,c,d,p,e)=(f7d2c329,fd3be488,d0007c70,0000a000,1,fdffc000).

The fixed prefixes have common W0..W5 and must satisfy

    D_s0(W6,a)=-p
    D_s0(W7,b)=e-a
    D_s0(W8,c)=-p-b
    D_s1(U,e)+D_s0(W9,d)+c=0.

Define the complete admitted left-word sets

    J14={V : D_s1(V,p)=-d and D_s0(V,p)=-e}
    J23={Z : D_s1(Z,-p)=-d and D_s0(Z,-p)=-e}.

The parent exact carry/borrow classification gives size 2^27 for each p4
set, and size N=138936320 for each p1 set. The p4 sets are affine of
dimension 27; the p1 sets are disjoint unions of components of dimensions
27,22,19. This packet reproduces the algebraic counts from the bound parent
module; it does not perform a 2^32 scan.

## 2. Trade W13 for a free W12

The preceding chart made common W10,W11,W13 free and repaired W12,W15.
The repaired W12 is a bijective function of W13 when V,Z,W10,W11 and the
context are fixed. Consequently the three consecutive common words
W10,W11,W12 can be free instead.

For any V in J14, Z in J23 and common W10,W11,W12, set W14=V and compute:

    W16=s1(V)+W9+s0(W1)+W0
    Q21=s1_inverse(Z-W16-s0(W8)-W7)
    Q19=s1_inverse(Q21-V-s0(W6)-W5)
    W17=s1_inverse(Q19-W12-s0(W4)-W3)
    W15=s1_inverse(W17-W10-s0(W2)-W1)
    W20=s1_inverse(U-W15-s0(W7)-W6)
    W18=s1(W16)+W11+s0(W3)+W2
    W13=W20-s1(W18)-s0(W5)-W4.

The small-sigma1 map is a bijection. Each inverse expression therefore has
one value, and there is no circular dependency. Forward expansion gives
W19=Q19, W21=Q21, W22=U and W23=Z.

Both repairs are common to the lanes. To see this, W16 is common by the
J14 condition. The argument defining Q21 is common by the row23 condition;
the argument defining Q19 is common by row21. Then W17 and W15 are common.
The row22 condition makes the argument defining W20 common, and W18 is
common, so W13 is common as well.

The remaining quiet rows follow from the fixed row24 condition, the two
J14/J23 joint predicates, and dW23+dW14=0. Thus the exact support through
W38 is retained. In particular

    dW37=D_s0(U,e) != 0,

and W38 is common. Nonzero follows from e!=0 and injectivity of s0.

Injectivity of the chart is immediate by reading W10,W11,W12,V from the
message and Z from its unique expansion. Conversely, every schedule in the
declared slice exposes those values, and the recurrence forces the displayed
repairs. This is a bijection, not merely a sufficient generator.

## 3. Replace the three common words by desired left outputs

At a fixed left state S_t=(a,b,c,d,e,f,g,h), the next left a output is

    A_t = h+Sigma1(e)+Ch(e,f,g)+K_t+W_t+Sigma0(a)+Maj(a,b,c).

For any desired A_t, solve exactly:

    W_t=A_t-h-Sigma1(e)-Ch(e,f,g)-K_t-Sigma0(a)-Maj(a,b,c).

The next left e output is

    E_t=d+A_t-Sigma0(a)-Maj(a,b,c).

Starting from the actual S10_left, use this equation sequentially for
t=10,11,12. It is a bijection between the three desired left A outputs and
the three common message words. The right lane uses those same words; its
outputs are consequences rather than separately selectable values.

Since the fixed prefix and all words through W12 are now fixed, both entire
state traces through S13 are fixed. Changing V,Z only changes W13,W14,W15
among initial words. All |J14|*|J23| choices are admissible and distinct.

The resulting exact partition is

    p4: 2^150 = 2^96 output triples x 2^54 S13-preserving completions.
    p1: N^2*2^96 = 2^96 output triples x N^2 completions.

The modular difference at S14 is also the same throughout each fixed-triple
fibre: round13 starts from fixed absolute states and consumes a common word.
That common word cancels from the difference of T1, so every component of
Delta S14 is fixed. The absolute states at S14 generally move with W13.

## 4. Exact conditional fibre preserving S14

Let T be a desired common W13. Equivalently, prescribe a left A13 and solve
its unit-coefficient equation at the fixed left S13 to obtain T.

For any proposed V, compute the ordinary recurrence in this order:

    W16=s1(V)+W9+s0(W1)+W0
    W18=s1(W16)+W11+s0(W3)+W2
    W20=s1(W18)+T+s0(W5)+W4
    W15=U-s1(W20)-s0(W7)-W6
    W17=s1(W15)+W10+s0(W2)+W1
    W19=s1(W17)+W12+s0(W4)+W3
    W21=s1(W19)+V+s0(W6)+W5
    H_T(V)=s1(W21)+W16+s0(W8)+W7.

The exact remaining set is

    V_T={V in J14 : H_T(V) in J23}.

Each accepted V gives exactly one completion, with Z=H_T(V). These
completions preserve BOTH absolute S14 states because both message prefixes
through W13 are fixed.

For p4 this is a conditional problem on 27 affine input bits, with five
exact affine membership equations applied to the output H_T(V). H_T itself
is nonlinear because of its modular additions and reconverging dependencies.
The five conditions cannot be assigned independent random-bit penalties.

For fixed V, Z <-> T is a bijection over the full 32-bit word domain by the
inverse chain in section2. Therefore restricting Z to J23 admits exactly
|J23| different T values for that V. This does not make V -> H_T(V) bijective
at fixed T; V enters several paths that reconverge.

## 5. Large S14 fibres exist, by counting

Write n(T)=|V_T|. Every V,Z tuple gives one T, and fixed V,T determines Z
uniquely. Hence, including empty fibres,

    sum over all 2^32 words T of n(T) = |J14|*|J23|.

For every admissible fixed context and every chosen left output triple:

| Arm | Exact average n(T), including empty fibres | Guaranteed existence |
|---|---:|---|
| p4 | 2^54 / 2^32 = 2^22 | Some T has at least 2^22 completions |
| p1 | N^2 / 2^32 = 4,494,400 | Some T has at least 4,494,400 completions |

The qualifying T can depend on the context. A preselected T may have an
empty fibre. No uniformity, direct parameterization of V_T, or fast listing
method is proved here.

There is also a precise sampling consequence for p4 that uses no random-SHA
model. Sample V,Z uniformly from their exact affine product, and take their
induced T. The fraction landing in fibres smaller than 2^21 is less than

    (2^32 * 2^21) / 2^54 = 1/2.

Thus at least half of the paired parameter tuples belong to S14 fibres with
at least 2^21 members. This is a statement about sampling the known chart;
it says nothing about endpoint success or the cost of certifying/listing
the other members of a sampled fibre.

## 6. Why this is not independent-lane freedom

Write t=(W10,W11,W12,V,Z) and its generated pair (L_t,R_t). Recombining
L_t with R_t' while keeping the retained oriented numerical differences
forces the three visible common words to agree. It also forces

    (V'+p)-V=p and (Z'-p)-Z=-p,

so V'=V and Z'=Z. Hence t'=t. The retained slice has a perfect-matching
interface under these predicates. Its 2^150 paired members cannot be
priced as independent left/right birthday opportunities.

Cross-pairs outside the retained pattern define a different question whose
schedule and state conditions would need to be derived separately.

## 7. Verification and research consequence

state_coordinates.py implements the new inverse construction and the
one-word conditional map. reference.py is the bound, separate forward
SHA-256 implementation, which does not import the constructor.

verify.py checks 384 admissible paired completions across both numerical
arms and three actual entry choices: literal standard IV, the public common
first block's C39, and that block's C40. It checks the chosen A outputs,
complete schedule support through W38, fixed U and dW37, identical paired
traces through S13, fixed Delta S14, and round trips through the preceding
W10,W11,W13 chart. It also checks 144 unrestricted Z/W13 inverse examples.
All pass. These are bounded implementation checks; the all-domain statements
come from the displayed bijections and exact fibre classification.

The useful next question is whether a selected conditional V_T admits an
explicit, inexpensive parameterization or useful state constraints beyond
S14. A specific late residual must eventually be controlled while preserving
the earlier conditions. No such endpoint control is established here.

For r39 the retained target remains the h-only S37 difference cancelling
dW37. For r40 the common-W39 extension remains excluded for these numerical
cores; final-round cancellation is a separate state target. This chart does
not alter either conclusion. A changed target round must use its actual
entry (C39 versus C40), rather than reuse a different-round chaining value.

The original reachable-S6 packet, the parent late-core packet, and the frozen
A/B/C comparison were not modified.
