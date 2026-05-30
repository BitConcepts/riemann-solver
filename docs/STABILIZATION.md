# Form Stabilization of the Truncated Weil Quadratic Form

## Summary

We observe empirically that the ground-state eigenvalue of the Connes-van
Suijlekom truncated Weil quadratic form QW_λ **stabilizes** as the prime
cutoff c increases, for fixed basis dimension N. This is consistent with
the theoretical prediction that for compactly supported test functions,
QW_λ(f) = QW(f) exactly once λ² exceeds the support.

## Theoretical Background

From the Weil explicit formula (Connes-Consani 2021, Selecta Math.):

For a test function f with supp(f) ⊂ [p⁻¹, p], the Weil quadratic form
decomposes as:

    QW(f) = W_∞(f) + Σ_{q prime, q ≤ p} W_q(f)

The sum involves **only finitely many primes** — those ≤ p. Therefore,
for the truncated form QW_λ with λ = √c:

    QW_λ(f) = QW(f)  for all c ≥ p

This is **exact equality**, not an approximation. The truncated form
literally stops changing once all relevant primes are included.

## Empirical Results

### Run 1: N=30, dps=50 (Phase 6 of full run)

| c  | log₁₀|λ_min| | Δ from prev |
|----|-------------|-------------|
| 7  | -27.1       | —           |
| 11 | -42.9       | 15.79       |
| 13 | -47.5       | 4.63        |
| 17 | -50.3       | 2.75        |
| 19 | -50.6       | **0.29**    |
| 23 | -51.4       | 0.80        |
| 29 | -50.2       | 1.23        |
| 31 | -50.3       | 0.18        |
| 37 | -50.7       | 0.36        |

**Observation**: After c=17, the eigenvalue enters a plateau band of
~1.2 OOM width [-51.4, -50.2]. The deltas drop from 15.79 to sub-1.
The stabilization criterion (last delta < 50% of first delta) is met.

### Run 2: N=100, dps=80 (Extended run — pending)

Higher N should sharpen the plateau because the Galerkin approximation
is more accurate. At N=30, the basis truncation introduces its own error.

## Significance for the Proof

The form stabilization has three consequences:

1. **The limit exists**: Since QW_λ stabilizes, lim_{λ→∞} QW_λ = QW
   is well-defined (trivially — it's exact equality for finite support).

2. **Criticality transfers**: By CCM Theorem 6.1 (Connes-van Suijlekom
   2025), all zeros of the truncated form's eigenvector Fourier transform
   lie exactly on the critical line, for every finite c.

3. **The gap narrows to identification**: If the zeros converge (which
   stabilization supports but does not prove), then by Hurwitz's theorem,
   the limit zeros are also on the critical line. The only remaining
   question is: are they the actual Riemann zeros?

## What This Does NOT Prove

- We do not prove that the zeros converge (step 6.5 of Connes' program)
- We do not identify the limit function with Ξ (step 6.6)
- The Galerkin truncation (finite N) adds its own error on top of the
  prime truncation (finite c), so the stabilization we observe is of
  the combined system, not the pure Weil form

## Connection to Slepian Theory

The stabilization rate may be related to the Shannon number N_c = 2c/π
from the Slepian-Laplace mapping (Ohzeki 2026). As c increases, the
information capacity of the Laplace channel grows, and the eigenvalue
cliff (where eigenvalues drop to negligible size) moves to higher index.
The stabilization occurs when the Shannon number exceeds the effective
degrees of freedom of the test function.

## References

- Connes & Consani (2021), "Weil positivity and trace formula, the
  archimedean place", Selecta Math. 27(4), 77.
- Connes, Consani & Moscovici (2025), arXiv:2511.22755, Theorem 6.1.
- Groskin (2026), arXiv:2605.20224, eigenvector c-invariance (overlap ≥ 0.95).
- Ohzeki (2026), arXiv:2605.26586, Slepian-Laplace mapping.
