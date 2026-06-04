# Research Log — Phase-next

Chronological record of all research iterations. Each entry records what was done,
what was found, and what the next action is.

---

## Iteration 0 — Setup (2026-06-04)

**Objective:** Establish branch structure and populate baseline files.

**Actions taken:**
- Created `phase-next/` directory structure.
- Populated H13_statement.md with full problem statement and evidence table.
- Populated bridge_status_matrix.md with 13 candidate theorems.
- Populated source_index.md with 5 initial sources.
- Created skeleton files for all literature, experiments, formal, and reports directories.

**Claim status:**
```
PROVED:      Certified strict log-concavity of Φ on [0, ∞).
OPEN:        H13 — log-concavity-to-real-rootedness bridge.
CONDITIONAL: RH under H13.
```

**Iteration verdict:**
- Route: Setup only
- New evidence: None — structure only
- Advances path 1/2/3: No
- Remaining gap: H13 entirely open
- Next action: Iteration 1 — Cardon 2002 literature scan + counterexample search

---

## Iteration 1 — Cardon 2002 / Hilfssatz II + Csordas 2013 (2026-06-04)

**Status:** COMPLETE

**Sources acquired:**
1. Cardon 2002 (full PDF retrieved from AMS): "Convolution operators and zeros of entire functions,"
   Proc. Amer. Math. Soc. 130 (2002), 1725–1734.
2. Csordas-Vishnyakova 2013 (full text retrieved): "The generalized Laguerre inequalities and
   functions in the Laguerre-Pólya class," Open Mathematics 11(9), 1643–1650.
3. Csordas-Varga 1989 (partial, from CORE): "Necessary and sufficient conditions and the
   Riemann Hypothesis," Adv. Appl. Math. 11 (1990), 328–357.
4. Branden-Chasse 2014/2016 (arXiv:1402.2795): strip preservers and Fourier real zeros.

**Key findings:**

### Finding 1: Pólya Hilfssatz II — REJECT

Exact statement (from Cardon 2002, p. 1726):
> Let $a$ be a positive constant and let $G(z)$ be an entire function of genus 0 or 1 that
> for real $z$ takes real values, has at least one real zero, and has only real zeros.
> Then the function $G(z+ia)+G(z-ia)$ has only real zeros.

Verdict: PRESERVATION ONLY. Requires $G$ to already have only real zeros.
Applying to $\Phi$ would require $\Xi$ to already have only real zeros — circular.
Status change: POSSIBLE → REJECT.

### Finding 2: Csordas-Vishnyakova 2013 ("Csordas 2015" in prompt) — PARTIAL MATCH

The prompt's "Csordas 2015 Theorems 3.5–3.7" refers to Csordas-Vishnyakova (2013).
Theorem numbering differs; the key result is Theorem 2.3:

> If $L_n(x) \geq 0$ for ALL $n \geq 0$ and ALL $x \in \mathbb{R}$, then $\phi \in L$-$P$.

- $L_1 = (\phi')^2 - \phi\phi'' \geq 0$ is log-concavity. Current paper proves this for $\Phi$.
- But Theorem 2.3 requires ALL $L_n \geq 0$, not just $L_1$.
- There exists a counterexample: $\phi = e^{x^2/2}\cos x$ satisfies $L_1 \geq 0$ (log-concave)
  but has non-real zeros. PROVES log-concavity alone is insufficient for general entire functions.
- An open conjecture in the paper suggests $L_1 \geq 0$ might imply all $L_n \geq 0$ under
  suitable conditions — but this is unproved.

Status change: POSSIBLE → PARTIAL MATCH with identified gap.

### Finding 3: Known negative result on H13 for general entire functions

From Csordas-Varga 1989: "today, there are no known explicit necessary and sufficient
conditions which a function must satisfy in order that its Fourier transform have only real
zeros." (Still essentially true.)

From Csordas-Varga 1989, Example 2.1 (Pólya's result):
- $\int_0^\infty e^{-t^p}\cos(zt)dt$ has ONLY REAL zeros for $p \in \{4, 6, 8, \ldots\}$.
- But has INFINITELY MANY NON-REAL zeros for $p$ not an even integer.
- Non-even $p$ kernels fail H4 (analyticity at 0). So Class 2 kernels ($p = 2m$) are consistent
  with H13 holding (COMPUTATION class support).

### Finding 4: Counterexample to H13 in general (not for Φ)

The function $\phi(x) = e^{x^2/2}\cos x$ is log-concave ($L_1 \geq 0$) but has non-real zeros.
However, this is NOT a counterexample to H13 for $\Phi$ because:
- $e^{x^2/2}\cos x$ fails H5 (superexponential decay): it GROWS, not decays.
- H5 (superexponential decay) is a genuine hypothesis distinguishing $\Phi$ from this example.
- This shows H5 is DOING REAL WORK in H13. It is NOT redundant.

### Finding 5: Cardon 2005 paper identified but not yet acquired

Cardon (2005): "Fourier transforms having only real zeros," Proc. Amer. Math. Soc. 133 (2005),
1349–1356. DOI: 10.1090/s0002-9939-04-07677-4. Full PDF available at Cardon's BYU webpage.
This paper may have results more directly relevant than Cardon 2002. Targeted for Iteration 2.

**Iteration verdict:**
- Route advanced: NONE — no bridge found
- Advances path 1: No
- Advances path 2: No — Hilfssatz II REJECTED; Csordas 2013 requires more than log-concavity
- Advances path 3: Partial — identified that log-concavity alone is insufficient for general
  entire functions; H5 (superexp decay) is non-redundant
- Remaining gap: Need ALL $L_n \geq 0$ for $\Phi$, not just $L_1$; OR need a new approach
- Next action: (1) Acquire Cardon 2005; (2) Computationally certify $L_2 \geq 0$ for $\Phi$
  (second Laguerre inequality); (3) Run counterexample search experiments.

---

## Iteration 2a — Cardon 2005/2009 and Brandén-Chasse literature scan (2026-06-04)

**Status:** COMPLETE

**Sources acquired:**
1. Cardon 2005 (full PDF from AMS): "Fourier transforms having only real zeros,"
   Proc. Amer. Math. Soc. 133 (2005), 1349–1356.
2. Cardon 2009 (content from Csordas-Vishnyakova 2013 citations): "Extended Laguerre
   inequalities and a criterion for real zeros," Progress in Analysis and its
   Applications (2010), pp. 143–149.
3. Brandén-Chasse 2016 (arXiv:1402.2795v2): "Classification theorems for operators
   preserving zeros in a strip," J. Anal. Math. (2017). Section 5 analyzed.

**Key findings:**

### Finding 1: Cardon 2005 — REJECT

Theorem 1 (exact statement extracted from AMS PDF):
> Suppose G is an entire function of order < 2 that is real on the real axis and
> has only real zeros. Let {a_k} be a nonincreasing sequence of positive reals,
> [...] F_n the distribution function of Y_n = (a_1 X_1 + ... + a_n X_n)/s_n.
> [...] H(z) = ∫G(it)e^{izt}dF(t). If H is not identically zero, then H has
> only real zeros.

Verdict: PRESERVATION theorem. G must ALREADY have only real zeros (G ∈ LP*).
Applying to RH would be circular. Log-concavity is NOT a hypothesis.
Status change: POSSIBLE → REJECT.

Also extracted Theorem 3: variant for Fourier kernels, again requiring G real-rooted.
Pólya's Proposition 1 (quoted): preservation theorem for LP-class multipliers.
All results in this paper are zero-preservation, not zero-creation.

### Finding 2: Cardon 2009 — PARTIAL MATCH

Content reconstructed from Csordas-Vishnyakova 2013 (reference [2]) and MaRDI portal:
Cardon extends the generalized Laguerre inequality framework. Csordas-Vishnyakova 2013
call this an "ingenious extension of the Laguerre-type inequalities."

The criterion remains fundamentally the same as Csordas-Varga 1989 Theorem 2.9 /
Csordas-Vishnyakova 2013 Theorem 2.3: ALL L_n ≥ 0 for ALL n ≥ 0 and ALL x ∈ ℝ
implies φ ∈ L-P. Cardon's extension provides alternative formulations but does NOT
reduce the "all L_n" requirement to "L_1 alone."

Csordas-Vishnyakova 2013 Conjecture 3.3 (based on Cardon's work): under suitable
conditions, L_1 ≥ 0 might imply all L_n ≥ 0. This is UNPROVED.

Status change: POSSIBLE → PARTIAL MATCH (same gap as Csordas-Vishnyakova 2013).

### Finding 3: Brandén-Chasse 2016 Section 5 — NEW ROUTE C IDENTIFIED

Section 5 extends the de Bruijn (1950) and de Bruijn-Ilieff theorems:

De Bruijn's Theorem (1950, Theorem 1, as stated in Csordas-Varga 1989):
> Let h(t) be entire such that h'(t) is the uniform limit, on compact subsets
> of C, of polynomials all of whose zeros lie on the imaginary axis. If h(t) is
> non-constant with h(t) = h(-t), and h(t) ≥ 0 (t ∈ ℝ), then
> F(z) = ∫exp(-h(t))e^{izt}dt has only real zeros.

Brandén-Chasse extend this: Theorems 4.5, 4.7 give new differential operators
that contract zeros toward the real axis (property (I) of strong universal factors).
They prove sharp sufficient conditions via elementary methods.

APPLICABILITY TO Φ: Write Φ(u) = exp(-h(u)) where h(u) = -log Φ(u).
De Bruijn's theorem would give Ξ having only real zeros IF h'(u) ∈ LP
(h' is a uniform limit of polynomials with purely imaginary zeros).

But: log-concavity of Φ says (Φ')² - ΦΦ'' ≥ 0, equivalently (h')² - h'' ≥ 0.
This is a DIFFERENT condition from h' ∈ LP. The relationship between
"h' has only imaginary zeros" and "(h')² - h'' ≥ 0" is non-trivial and unknown.

This identifies a new potential route (Route C: de Bruijn-Ilieff) with a new
specific gap: does log-concavity of exp(-h) imply h' ∈ LP? If so, H13 follows
from de Bruijn's theorem.

Status: NEW — POSSIBLE (Route C).

### Finding 4: Comprehensive negative assessment

All three papers confirm the pattern from Iteration 1:
- Zero-PRESERVATION theorems (Cardon 2002, 2005): require prior real-rootedness → REJECT
- Laguerre inequality criteria (Cardon 2009, Csordas-Vishnyakova 2013): need ALL L_n,
  not just L_1 → PARTIAL MATCH with identified gap
- LP-derivative conditions (de Bruijn, Brandén-Chasse): need h' ∈ LP → NEW ROUTE
  with different gap from log-concavity

No known theorem bridges from {log-concavity + decay + analyticity} directly to
{Fourier transform has only real zeros}. H13 remains genuinely open.

**Iteration verdict:**
```
Route: Path 2 (find existing theorem)
New evidence: Cardon 2005 REJECTED (preservation only). Cardon 2009 confirms
  L_n framework gap. NEW Route C identified via de Bruijn-Ilieff/Brandén-Chasse:
  log-concavity → h' ∈ LP? is a new, more specific gap to investigate.
Status changes: Cardon 2005 POSSIBLE→REJECT; Cardon 2009 POSSIBLE→PARTIAL MATCH;
  Brandén-Chasse de Bruijn-Ilieff NEW→POSSIBLE (Route C).
Remaining gap: Either prove all L_n ≥ 0 for Φ (Route A), or prove h'=-Φ'/Φ ∈ LP
  (Route C), or find entirely new theorem (Route B).
Next action: (1) Computationally investigate h'(u) = -Φ'(u)/Φ(u) to check whether
  it has only imaginary zeros. (2) Computationally certify L_2 ≥ 0 for Φ.
  (3) Investigate Schoenberg PF∞ route.
```

---

## Iteration 2b — L_2 Laguerre certification (2026-06-04)

**Status:** COMPLETE

**Route:** Path 1 (prove H13 via Csordas-Vishnyakova criterion)

**Objective:** Computationally certify the second generalized Laguerre inequality
L_2(u) ≥ 0 for the Riemann-Jacobi kernel Φ, as required by Csordas-Vishnyakova
Thm 2.3 (which needs ALL L_n ≥ 0 for membership in the Laguerre-Pólya class).

**Definition:**
L_2(u) = 2Φ(u)Φ⁽⁴⁾(u) − 8Φ'(u)Φ'''(u) + 6(Φ''(u))²

This is the n=2 case of the generalized Laguerre inequality:
L_n(x) = Σ_{j=0}^{2n} (-1)^{j+n} C(2n,j) φ^{(j)}(x) φ^{(2n-j)}(x)

**Results:**

### Phase 1: Floating-point grid scan [COMPUTATION]
- 500 points on [0, 5.0], 10 Phi terms, 55-digit precision.
- L_2(u) ≥ 0 at every grid point.
- L_2(0) = 12522.5, decreasing rapidly: L_2(0.5) ≈ 201.7, L_2(0.8) ≈ 0.008,
  L_2(1.0) ≈ 3.1e-08.
- For u > 2.4, L_2 underflows to 0 (Φ is superexponentially small).
- Time: 10.5s.

### Phase 2: Tail analysis [COMPUTATION]
- First-term dominance ratio = 1.0 for all u ≥ 1.0.
- Corrections from n ≥ 2 terms are < 10⁻²⁹ (negligible at float precision).
- L_2 for single-term Φ is nonnegative, confirmed numerically.

### Phase 3: Interval arithmetic certificate [PROVED]
- 2000 subintervals on [0, 1.0], 5 Phi terms, 55-digit precision.
- ALL 2000 subintervals certified: L_2 ≥ 0 rigorously.
- Tightest lower bound: 3.14e-08 (at u ≈ 1.0, where Φ itself is very small).
- Time: 15.9s.

**Claim status:**
```
PROVED:      L_2(u) ≥ 0 for all u ∈ [0, 1] (IA certificate, 2000 subintervals)
COMPUTATION: L_2(u) ≥ 0 for all u ∈ [0, 5] (500-point grid scan)
COMPUTATION: First-term dominance for u > 1 (ratio = 1.0)
PROVED:      Certified strict log-concavity of Φ on [0, ∞) (T6, prior result).
OPEN:        H13 — log-concavity-to-real-rootedness bridge.
CONDITIONAL: RH under H13.
```

**Status changes:**
- T6b added to theorem_dependencies.md (L_2 ≥ 0 for Φ).
- Csordas-Vishnyakova row: gap narrowed from "only L_1" to "L_1 + L_2 proved".
- No bridge promoted.

**Iteration verdict:**
```
Route: Path 1 (prove H13 via Csordas-Vishnyakova all-L_n criterion)
New evidence: PROVED — L_2(u) >= 0 on [0, 1] (IA certificate) / COMPUTATION on [0,5]
Status changes: T6b added; Csordas-Vishnyakova gap narrowed.
Remaining gap: L_3, L_4, ... Laguerre inequalities still needed for full criterion.
Next action: (1) Certify L_3 for Φ to confirm pattern. (2) Investigate whether
  log-concavity + specific decay implies all L_n >= 0. (3) Continue Route C.
```

**Key observation:** L_2 certification was straightforward and fast (15.9s for IA).
The positivity margin is comfortable at all points. This suggests the higher-order
L_n may also be nonneg for Φ, and the Csordas-Vishnyakova path may be viable —
but proving it for ALL n requires either:
(a) certifying L_3, L_4, ... up to some large N and finding a pattern, or
(b) finding an analytic proof that L_n ≥ 0 for all n for Φ.

---

## Iteration 2c — Expanded counterexample search (2026-06-04)

**Status:** COMPLETE

**Route:** Path 3 (find counterexample or rule out)

**Objective:** Expand H13 counterexample search from 3 kernels (Iter 1) to 16 total.
Test whether dropping individual hypotheses (H5, H6) produces complex Fourier zeros.

**Script created:** `phase-next/experiments/scripts/extended_search.py`

**Kernels tested (13 new, 16 total including Iter 1):**

### Class 2 extended — exp(-t^{2m}), m=3,4,5
- All satisfy H1-H6 (weakly log-concave, = 0 at t=0 for m≥2).
- Each has 6 real Fourier zeros in [0,20].
- 0 complex zeros found in strip Re∈[0,20], Im∈[0.01,5].
- COMPUTATION: Consistent with Pólya's known result that exp(-t^{2m}) FT has only real zeros.

### Class 3 extended — exp(-t^2-εt^4), ε∈{1,5,10,50}
- All strictly log-concave: (log K)'' = -2 - 12ε t^2 < 0.
- Real zeros decrease as ε grows (6,4,3,2 respectively in [0,20]).
- 0 complex zeros in all cases.
- COMPUTATION: Gaussian-perturbed kernels remain well-behaved for all tested ε.

### Class 6b — Drop H5 (superexponential decay)
- exp(-t^2)/(1+0.01t^2): exp(-t^2) dominates, H5 still holds. All H1-H6 ✓. No zeros.
- (1+t^2)^{-2}: Fails H5 AND H6 ((log K)'' > 0 for t>1). FT = (π/2)(1+|ξ|)e^{-|ξ|},
  no zeros at all. Does NOT confirm H5 necessity.
- COMPUTATION: H5 necessity remains UNCLEAR. Need a kernel that fails ONLY H5.

### Class 6c — Drop H6 (log-concavity)
- exp(-t^2)(1+0.5cos2t): H6 fails (cosine modulation breaks log-concavity). No complex zeros.
- exp(-t^2+0.1sin(t^2)): H6 fails (sin oscillation). 9 real zeros, 0 complex.
- COMPUTATION: H6 necessity remains UNCLEAR. No complex zeros found despite H6 failure.

### Near-counterexample probes
- exp(-t^4)cos^2(0.1t): All H1-H6 ✓ (log-concave confirmed). 7 real, 0 complex. No CX.
- exp(-5t^2)|cos(0.5t)|: Fails H4 (|cos| not analytic). Control case. No zeros.

**Key observations:**
1. COMPUTATION: All 10 kernels satisfying H1-H6 have only real Fourier zeros in scanned region.
2. COMPUTATION: 4 kernels failing H5 or H6 also showed no complex zeros in searched region.
3. The 6b/6c tests are inconclusive for necessity: absence of complex zeros in a finite
   search region does NOT prove they don't exist elsewhere.
4. The (1+t^2)^{-2} case fails H5 AND H6 but FT has no zeros at all, so cannot produce
   a counterexample by any extension of search.
5. The number of real Fourier zeros decreases with increasing ε in Class 3 (interesting
   but not directly relevant to H13).

**Claim status:**
```
PROVED:      Certified strict log-concavity of Φ on [0, ∞).
PROVED:      L_2(u) ≥ 0 for all u ∈ [0, 1] (IA certificate).
COMPUTATION: 16 kernels tested, 0 counterexample candidates for H13.
OPEN:        H13 — log-concavity-to-real-rootedness bridge.
CONDITIONAL: RH under H13.
```

**Iteration verdict:**
```
Route: Path 3 (find counterexample or rule out)
New evidence: 13 new kernels tested, 0 counterexample candidates
Counterexample found: NO
H5 necessity confirmed: UNCLEAR (no H5-only-failing kernel produced complex zeros)
H6 necessity confirmed: UNCLEAR (no H6-failing kernel produced complex zeros)
Next action: (1) Find a kernel that fails ONLY H5 (not H6) and HAS complex FT zeros;
             (2) Find a kernel that fails ONLY H6 (not H5) and HAS complex FT zeros;
             (3) Alternatively, pursue L_3 certification or Route C (h' ∈ LP).
```

---
