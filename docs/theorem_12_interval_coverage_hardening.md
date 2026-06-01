# Deliverable: theorem_12_interval_coverage_hardening.md
# Task 3 — Theorem 5 (Extended Cert [1,3]) Interval Coverage

## What the Script Does (Explicitly)

`proof/verify_ia_1_to_1_5.py` with the endpoint-coverage fix applied:

For each i = 0, 1, ..., 100:
  - Sets u_i = 1.0 + i × 0.02
  - Evaluates W₁ on the **interval** I_i = [u_i − 0.01, u_i + 0.01] using mpmath.iv
    at 60-digit precision: computes an **interval enclosure** W₁_iv containing the
    true value of W₁(u) for every u ∈ I_i.
  - Evaluates ε(u) = Σ_{n=2}^{15} n⁴ e^{−π(n²−1)e^{2u}} on I_i using interval arithmetic:
    computes an **interval enclosure** ε_iv satisfying ε_iv.upper ≥ sup_{u∈I_i} ε(u).
  - Verifies: W₁_iv.upper + 204 × ε_iv.upper < 0
    (If true: certifies that W₁(u) + 204·ε(u) < 0 for ALL u ∈ I_i, not just the midpoint.)

**Certified quantity per interval:** For every u ∈ I_i:
  W₁(u) ≤ W₁_iv.upper  (true by IA enclosure property)
  204·ε(u) ≤ 204·ε_iv.upper  (true by IA enclosure property)
  → W₁(u) + 204·ε(u) ≤ W₁_iv.upper + 204·ε_iv.upper < 0  ✓

## Coverage Guarantee

Consecutive intervals overlap:
  I_i = [u_i − 0.01, u_i + 0.01]  with spacing 0.02 between centers
  I_{i+1} = [u_{i+1} − 0.01, u_{i+1} + 0.01] = [u_i + 0.01, u_i + 0.03]

The union ∪ I_i = [1.0 − 0.01, 3.0 + 0.01] = [0.99, 3.01] ⊃ [1.0, 3.0].

**Complete interval tiling: every u ∈ [1.0, 3.0] is contained in at least one I_i.** ✓

## Result from results/verify_ia_1_to_1_5.json

- n_checkpoints: 101
- certified: 101
- failed: 0
- min_margin: 93.149 (at u = 1.0, half-width = 0.01)
- dps: 60
- perturbation_C: 204
- all_certified: true
- SHA256 of output file: 7D65253C5A8FA397FD83684A7A90978A71731552E073E4197DE543A894097F32

## Required Paper Text Addition

The following sentence must be explicit in Theorem 5's proof:

> For each i, the script evaluates interval enclosures W₁(I_i) and ε(I_i) using
> mpmath.iv at 60-digit precision, then verifies upper(W₁(I_i)) + 204·upper(ε(I_i)) < 0.
> Adjacent intervals overlap; their union covers [0.99, 3.01] ⊃ [1.0, 3.0], certifying
> the entire continuum, not merely 101 sample points.
> The minimum certified margin is 93.1 (at u = 1.0, interval [0.99, 1.01]).

## Acceptance Criterion

✓ The reader can see that each checkpoint is an **interval check**, not a point check.
✓ Full [1.0, 3.0] coverage is explicitly stated.
✓ The tiling argument (overlapping intervals covering the continuum) is stated.
