# Ideas from the HAWK and AES papers for the reachable sparse SHA-256 families

Date: 2026-11-09.

## Assessment

The useful direction is an exact simplification of a specified conditional interface. The existing charts give us genuine messages, a reachable common entry, and a known preservation depth. The next question is whether a parameter changes a required observable in a way that can be normalized, inverted, filtered, or reused more cheaply than evaluating every completion.

This packet derives an exact normalized representation of the local P,Q map, an inverse coordinate from two middle schedule words, and a precise condition for changing the order of two filters. These are useful objects for a future experiment. They establish neither an endpoint nor a speed improvement. The frozen A/B/C experiment is unchanged.

## Sources and what is transferable

All three supplied PDFs were read, including the technical appendices. Their original URLs and SHA-256 digests are in SOURCES.json.

| Source | Relevant sections | Transfer to investigate |
|---|---|---|
| HAWK-n Key Recovery Reduces to SVP in Dimension n/2 + 1, 29 pages | §§4–6; Appendix D | Replace a difficult searched object by a transformation with accessible constraints, and prove its useful structure. |
| Cryptanalysis of 7-Round AES via the Algebraic Structure of its S-box, 45 pages | §4; §5.5; Appendices A and D | Normalize a nuisance action at a particular comparison boundary, retaining reconstruction and actual cost. |
| Mythos Preview's Chain of Thought in Discovering the AES Möbius Bridge, 76 pages | §§3.4–3.5, 4.1, 7.2–7.4 | Test whether a projected description contains enough information; distinguish failure of a proposed propagation rule from a general impossibility. |

The AES bridge relates two multisets by an affine action after a field-inversion transformation. HAWK constructs a public cocycle lattice and proves its geometry. SHA has no established counterpart to either structure. The edited discovery record ends with unsuccessful approaches and broader negative conclusions; the final AES construction is the authority for the successful result.

The application below is our own derivation from the retained SHA equations. None of the source papers claims these SHA results.

## 1. Exact local normalization

All word arithmetic is modulo 2^32. Uppercase Sigma denotes the SHA-256 round rotations; lowercase sigma denotes the schedule functions. A fixed outer context and T=W13 determine both ordered S14 states. Put V=W14_left. The retained states have the form

\[
S_{15,L}=(V+\alpha_L,b_L,c_L,d_L,V+\beta_L,f_L,g_L,h_L),
\]
\[
S_{15,R}=(V+\alpha_R,b_R,c_R,d_R,V+\beta_R,f_R,g_R,h_R).
\]

The constants include the prescribed right-minus-left W14 difference. The ordered difference delta=Delta S15 is fixed. The next differential is

\[
\Delta S_{16}=(Q+P,\delta_a,\delta_b,\delta_c,
\delta_d+Q,\delta_e,\delta_f,\delta_g),
\]

with

\[
P(V)=\Sigma_0(V+\alpha_R)-\Sigma_0(V+\alpha_L)
+\operatorname{Maj}(V+\alpha_R,b_R,c_R)
-\operatorname{Maj}(V+\alpha_L,b_L,c_L),
\]

\[
Q(V)=\delta_h+\Sigma_1(V+\beta_R)-\Sigma_1(V+\beta_L)
+\operatorname{Ch}(V+\beta_R,f_R,g_R)
-\operatorname{Ch}(V+\beta_L,f_L,g_L).
\]

The common repaired W15 cancels from this immediate differential. It still affects absolute states and subsequent rounds.

### 1.1 Remove the input origin

Define

\[
x=V+\alpha_L,\quad d_a=\alpha_R-\alpha_L,\quad
d_e=\beta_R-\beta_L,\quad \kappa=\beta_L-\alpha_L.
\]

Then the two a inputs are x,x+d_a and the two e inputs are x+kappa,x+kappa+d_e. The absolute origin alpha_L is now outside the local evaluator.

### 1.2 Separate fixed masks and output offsets

For any word x, two exact identities are

\[
\operatorname{Maj}(x,b,c)=(b\mathbin{\&}c)+
(x\mathbin{\&}(b\oplus c)),
\]

\[
\operatorname{Ch}(x,f,g)=g+
(x\mathbin{\&}(f\mathbin{\&}\neg g))-
(x\mathbin{\&}(\neg f\mathbin{\&}g)).
\]

The majority summands have disjoint bits. For choice, the positive mask adds selected bits where g is zero; the negative mask removes selected bits where g is one. Thus these integer-word identities introduce no approximation. Complements are restricted to 32 bits.

For lane ell in {L,R}, define

\[
m_\ell=b_\ell\oplus c_\ell,\qquad
r_\ell=f_\ell\mathbin{\&}\neg g_\ell,\qquad
s_\ell=\neg f_\ell\mathbin{\&}g_\ell.
\]

Define output offsets

\[
c_P=(b_R\mathbin{\&}c_R)-(b_L\mathbin{\&}c_L),\qquad
c_Q=\delta_h+g_R-g_L.
\]

The normalized functions are

\[
\widehat P(x)=\Sigma_0(x+d_a)-\Sigma_0(x)
+((x+d_a)\mathbin{\&}m_R)-(x\mathbin{\&}m_L),
\]

and, writing y=x+kappa,

\[
\begin{aligned}
\widehat Q(x)={}&\Sigma_1(y+d_e)-\Sigma_1(y)\\
&+((y+d_e)\mathbin{\&}r_R)-((y+d_e)\mathbin{\&}s_R)\\
&-(y\mathbin{\&}r_L)+(y\mathbin{\&}s_L).
\end{aligned}
\]

Therefore

\[
P(V)=c_P+\widehat P(V+\alpha_L),\qquad
Q(V)=c_Q+\widehat Q(V+\alpha_L).
\]

The nine-word descriptor

\[
\mathcal K_{PQ}=(d_a,d_e,\kappa,m_L,m_R,r_L,s_L,r_R,s_R)
\]

is a sufficient representation of the normalized unrestricted function. Equal descriptors imply equal normalized functions. The converse is not claimed. For example, d_a=0 and m_L=m_R make P-hat identically zero independently of that common mask. This is not a minimal classification, an entropy count, or nine independent parameters.

### 1.3 Admissibility and target must be transported too

The actual domain remains

\[
\mathcal V_{\theta,T}=
\{V\in J_{14}:H_{\theta,T}(V)\in J_{23}\}.
\]

In normalized coordinates it becomes

\[
\widetilde{\mathcal V}_{\theta,T}=
\{V+\alpha_L:V\in\mathcal V_{\theta,T}\}.
\]

For targets Delta A15=u, Delta E15=v, the normalized target is

\[
(u-v+\delta_d-c_P,\quad v-\delta_d-c_Q).
\]

The same nine-word descriptor permits reuse of the unrestricted local evaluator. Reusing an admissible image/fibre certificate additionally requires an exact relation between the translated domains and targets. A table of unrestricted preimages could be reused across different domains only by reapplying each domain's filter. Endpoint reuse requires a further continuation argument.

The input translation is a bijective coordinate change. It removes no candidate by itself. The cost of producing the descriptor, listing admissible inputs, and reconstructing completions remains.

## 2. Two middle words recover the remaining coordinate

There is a useful exact consequence of row 29. In the fixed-T, fixed-U context, U=W22_left and V=W14_left:

\[
W_{29}=\sigma_1(W_{27})+U+\sigma_0(V)+T.
\]

Since the small sigma0 map is invertible,

\[
\boxed{V=\sigma_0^{-1}\bigl(W_{29}-\sigma_1(W_{27})-U-T\bigr).}
\]

This has two uses. If a construction has already determined W27 and W29, it can recover V exactly. It need not guess V independently. Conversely, holding those two absolute common words fixed cannot leave more than one V in the conditional chart. Once V is recovered, Z=H_T(V) and all repair words are fixed by the context.

Thus the map from V to the entire middle word tuple W24..W36 is injective within this fixed context. A cache that assumes an identical middle word tuple across distinct V has no multiplicity to exploit there.

This does not show that different word tuples induce different state permutations. It also does not cover changes to U,T or the outer context. Nor does it make arbitrary W27,W29 independently realizable. Their values must still come from a valid full schedule.

## 3. The S24 conjugation: exact structure and its limitation

For one fixed candidate schedule let B be the working-state permutation for the common rounds 24..36, and let d=Delta W37, which is nonzero. The r39 condition is

\[
S_{24,R}=B^{-1}H_{-d}B(S_{24,L}),
\]

where H shifts only h. This relation is exact, but computing its right-hand side currently involves the candidate's middle permutation.

On the full 256-bit working-state space, the conjugated transformation has order

\[
2^{32}/\gcd(d,2^{32}),
\]

and no fixed points. Let g=gcd(d,2^32). A complete invariant of its ambient orbits is

\[
I_B(s)=\bigl(B(s)[a..g],\ B(s)[h]\bmod g\bigr).
\]

Proof: repeated translations by d preserve the first seven words, and their h values range over exactly one residue class modulo g. Conjugating by B transports these orbits bijectively.

An orbit match permits any number of translation steps. The endpoint asks for exactly one prescribed step, namely h_R-h_L=-d after B. Therefore even a complete orbit invariant needs an exact displacement check. Moreover, I_B is not cheap merely because it has a formula: it still uses B. These ambient orbits need not preserve the reachable-prefix subset or the admitted chart.

A useful bridge would require a cheaper necessary observable, or a compact representation with a recovery rule, while retaining the candidate-dependent schedule. No such bridge has been proved here.

## 4. A practical filter-order experiment, with a fair baseline

Suppose a constant immediate target (u,v) is justified by a path condition or a valid backward relation. Define p*=u-v+delta_d and q*=v-delta_d. The target set is exactly

\[
\{V\in J_{14}: P(V)=p_*,\ Q(V)=q_*,\ H_T(V)\in J_{23}\}.
\]

P,Q need no evaluation of H_T. Testing the local target before computing the repair-admissibility map therefore preserves the intersection exactly. Whether it is cheaper is a separate question.

Let m=|J14|, n=|V_T|, and s be the number of V in J14 satisfying the local P,Q target. Let c_H include H and J23 membership, and c_PQ include the local target test. Under constant per-test costs:

| Order | Predicate work |
|---|---|
| Evaluate both unconditionally | m(c_H+c_PQ) |
| Admissibility first, short-circuit | m c_H+n c_PQ |
| Local target first, short-circuit | m c_PQ+s c_H |

The local-first order beats the stronger short-circuit baseline exactly when

\[
(m-s)c_H>(m-n)c_{PQ}.
\]

These are exact counts for a declared context and target, not random-bit estimates. Setup, enumeration, shared intermediate calculations, variable test costs, memory, and continuation must be added. If the backward target is candidate-dependent and costs H or B to determine, the early-test advantage may disappear.

An arbitrary local target does not establish progress toward r39 or r40. Its terminal relevance is the first requirement for this experiment.

## 5. What to attempt next

The following work is separate from the frozen formulation comparison.

1. Choose a partial condition required by the actual r39 or r40 boundary. Retain every condition used to derive it, including any dependency on V or the middle schedule.
2. Express that condition using the normalized local map, the row-29 inverse coordinate, or another exact boundary relation.
3. For a proposed equivalence between contexts, specify the input map, the output map, and the admitted domains. Prove domain preservation and covariance before sharing fibre counts.
4. Determine an exact target image or preimage rule on a bounded declared slice. A proof of emptiness is useful; a successful preimage rule is useful; nominal output variation alone is insufficient.
5. Measure complete work against the strongest equivalent baseline. Count failed admissibility tests, normalization, reconstruction, collisions in a filter, memory traffic, and scalar verification.

A proposed compressed state descriptor J is sufficient for a continuation projection E only if

\[
J(V)=J(V')\Longrightarrow E(V)=E(V')
\]

for all admitted members in the declared context. Fixed Delta S15 cannot simply be treated as a closed description of the later differential: the next state depends on P(V),Q(V). Any counterexample must itself satisfy the full admitted-domain predicates when it is used to refute a claim about that domain.

Likewise, an affine basis for J14 does not establish that arbitrary basis moves preserve H_T(V) in J23. Gray-code traversal may simplify enumeration, but incremental schedule/state savings require an explicit dependency analysis. Carry-conditioned algebra can help expose special cases, without a blanket claim that all resulting conditions are affine or cheap.

## 6. Existing conclusions retained

- Paired-family cardinality does not become independent left-times-right opportunity count.
- The same-aligned common-S15 through S22 obstruction for the two numerical cores remains.
- The common-W38/common-W39 schedule extension remains excluded for both numerical cores.
- r39 feasibility at the retained real entry is unresolved after the reported UNKNOWN query.
- r40 work must retain a live final compensator or change the numerical core/support.
- These local identities apply to actual fixed entries, but do not construct a late return from them.
- No endpoint distribution, probability, or Yukon exponent follows from this packet.

## 7. Verification and reproduction

The derivations above are algebraic. The executable checks verify their implementation on bounded inputs:

- Six previously retained admissible schedule pairs: both numerical arms, each under standard IV, public C39 and public C40. Raw messages are expanded, their support and numerical differences are checked, and states are replayed through S16.
- Six row-29 coordinate recoveries.
- A two-sided GF(2) inverse check for small sigma0 on all 32 basis vectors, 64 compositions total.
- 2,048 arbitrary contexts checking the normalized P,Q identity.
- 256 synthetic changes of input origin checking the local covariance identity.

The arbitrary contexts and origin changes are algebra controls. They are not asserted to be admissible or reachable schedule members. No solver, endpoint search, exhaustive word scan, or new empirical success estimate is used.

Run:

```bash
python3 -I -B checks/verify.py
```

Its output reproduces checks/RESULTS.json. Bound original fixture and scalar-reference copies are in checks/INPUTS.json and checks/reference.py; their hashes and provenance are in checks/SOURCE_BINDINGS.json. The new local implementation is checks/normal_form.py. The original research packets are unchanged.

## References

1. Z. Straznickas and S. A. Weis, HAWK-n Key Recovery Reduces to SVP in Dimension n/2 + 1. https://assets.claude.com/e8d50c167ad47beeb03d6109a4a484be95cb38ea.pdf
2. M. Nasr and N. Carlini, Cryptanalysis of 7-Round AES via the Algebraic Structure of its S-box. https://assets.claude.com/c88771e1bf5ee8885349eed05e5484c0e5f7e02b.pdf
3. Anthropic, Mythos Preview's Chain of Thought in Discovering the AES Möbius Bridge. https://assets.claude.com/5273e714527440f1c8b7c7bf5756d4ac22ae8995.pdf
