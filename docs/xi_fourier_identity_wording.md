# Deliverable: xi_fourier_identity_wording.md
# Task 5 — F(z) = 2Ξ(z) Identity: Analytic Continuation

## Problem

Remark 2 writes F(z) = ∫_{-∞}^{∞} Φ(u)e^{izu}du = 2Ξ(z) using evenness of Φ.
But the definition of Ξ(t) in equation (2) is for real t. The equality F(z) = 2Ξ(z)
for complex z requires justification via analytic continuation.

## Corrected Wording

Replace the one-line identity in Remark 2 with:

---
For real t, evenness gives:
  F(t) = ∫_{-∞}^{∞} Φ(u)e^{itu}du = 2∫_0^{∞} Φ(u)cos(tu)du = 2Ξ(t).

Both F(z) and z ↦ 2Ξ(z) are entire functions of z (F(z) is entire because Φ decays
super-exponentially as |u| → ∞, ensuring uniform convergence on any compact subset
of ℂ; Ξ(z) = ξ(1/2 + iz) is entire by the standard functional equation for ξ).
Since they agree on the real line, they agree on all of ℂ by the identity theorem
for analytic functions.

Therefore: F(z) = 2Ξ(z) for all z ∈ ℂ.

In particular, F has only real zeros if and only if Ξ has only real zeros (since
multiplication by 2 does not alter zeros).
---

## Why This Matters

Without this statement, a reviewer could object: "You apply Pólya's theorem to get
'F has only real zeros', but F is defined as a Fourier integral while your conclusion
is about the zeros of Ξ, an entirely different function. Where is the bridge?"

The analytic continuation argument provides that bridge explicitly.

## Acceptance Criterion

✓ The equality F = 2Ξ is established for complex z, not merely real t.
✓ The analytic continuation step is made explicit.
✓ Entiredness of both sides is justified.
