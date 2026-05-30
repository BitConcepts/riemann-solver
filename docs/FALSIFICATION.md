# Falsification Strategy

## Philosophy

> "The Riemann Hypothesis is probably true, but we must try as hard as
> possible to prove it false." — paraphrasing Popper

A mathematically honest investigation requires active falsification.
Numerical evidence supporting RH is abundant (10^13+ zeros verified),
but analytic number theory has many conjectures that are true up to
very large numbers but ultimately false (e.g., Skewes number phenomena).

---

## Method 1: Off-Critical-Line Zero Search

**Goal**: Find ρ with ζ(ρ) = 0 and Re(ρ) ≠ 1/2.

**Approach**: Systematic grid search in the critical strip 0 < σ < 1,
with σ ≠ 1/2, evaluating |ζ(σ + it)| at high precision.

**Grid design**:
- σ values: 0.01, 0.02, ..., 0.49, 0.51, ..., 0.99
- t values: adaptive spacing based on local zero density
- Precision: 60+ decimal digits
- Threshold: |ζ(s)| < 10^(-20) triggers refinement

**Known constraints**: By Bohr-Landau, for any ε > 0, the number of zeros
with Re(ρ) > 1/2 + ε and |Im(ρ)| < T is O(T). Most zeros cluster near
the critical line regardless of RH.

---

## Method 2: Li Coefficient Sign Monitoring

**Goal**: Find n such that λ_n < 0.

**Approach**: Compute λ_n using the Coffey formula to high precision.
If RH is true, λ_n grows like n log n. If false, λ_n eventually
oscillates with exponentially growing amplitude.

**Diagnostic**: Plot λ_n / (n log n) — under RH this converges to 1/2.
Deviation from this asymptotic is a warning signal.

---

## Method 3: Lehmer Pair Escalation

**Goal**: Find zero pairs so close together that Λ > 0 is forced.

**Approach**: The Csordas-Smith-Varga inequality bounds Λ from below
using close pairs of consecutive zeros (Lehmer pairs). Historical
bounds from ever-tighter pairs:

    -50 (1988) → -5 (1991) → -10^{-6} (1994) → -10^{-9} (2000) → 0 (2018)

The Rodgers-Tao proof established Λ ≥ 0 unconditionally. To disprove
RH, one would need a Lehmer pair implying Λ > 0 strictly. This requires
two consecutive zeros γ_k, γ_{k+1} with (γ_{k+1} - γ_k) extremely
small relative to the average spacing.

---

## Method 4: Gram Violation Analysis

**Goal**: Detect anomalous patterns in Gram's law exceptions.

Gram's law states that (-1)^n Z(g_n) > 0 where g_n are Gram points.
Exceptions are well-studied but any systematic structure in their
distribution could indicate deeper phenomena.

---

## Method 5: Davenport-Heilbronn Control (CRITICAL)

**Goal**: Verify that our falsification methods actually WORK by
testing them on a function where the generalized RH is KNOWN TO FAIL.

The Davenport-Heilbronn function is a Dirichlet series that satisfies
a functional equation but has zeros OFF the critical line. Our
off-line search method MUST successfully find these zeros.

If our falsification methods cannot find known off-line zeros of the
DH function, they cannot be trusted to find hypothetical off-line
zeros of ζ(s) either.

**Protocol**:
1. Implement DH function evaluation
2. Run off-line search → must find off-line zeros
3. Run Li-criterion analog → must detect sign changes
4. Only then trust these methods on ζ(s) itself

---

## Reporting

All falsification results MUST be reported with:
- Method used
- Search parameters (precision, grid, range)
- Negative result statement (no counterexample found)
- Precision limitations acknowledged
- DH control test results
