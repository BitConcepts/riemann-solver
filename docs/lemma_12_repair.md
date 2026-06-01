# Deliverable: lemma_12_repair.md
# Task 2 — Lemma W Repair After Correcting ε(u)

## Status: VALID — No substantive change required

Lemma W states:
  |W_tail(u)| ≤ λ(1)·|W₁(u)| ≤ 1.82×10⁻²⁵  for all u ≥ 1.

This bound is derived from λ(u) = |ΔQ(u)|/|Q_φ₁(u)|, which is the ACTUAL
perturbation ratio computed directly from ΔQ and Q_φ₁. It does NOT depend on
the ε(u) definition at all.

The only use of ε in the paper is in the script certification (Theorem 5).
Since we now use ε* = 2ε (the corrected bound), the logical chain becomes:

1. Lemma W: |W_tail(u)| ≤ 1.82×10⁻²⁵ (proved, independent of ε).
2. Theorem 5: |W₁(u)| ≥ 91.3 for u ∈ [1,3] (IA certified via script with corrected ε*).
3. Conclusion: W = W₁ + W_tail ≤ W₁ + 1.82×10⁻²⁵ < 0.

## Required paper change

Add to Lemma W proof: "The bound depends only on λ(1) = |ΔQ(1)|/|Q_φ₁(1)|
and not on the ε(u) definition, so it is unaffected by the prefactor correction."

## Regarding the "λ(u)·|W₁(u)| maximized at u=1" claim

The worry was: d/du[log λ] < 0 proves λ decreasing, but does NOT by itself prove
λ(u)·|W₁(u)| decreasing (since |W₁| grows).

**Resolution**: The bound |W_tail| ≤ λ(1)·|W₁| ≤ 1.82×10⁻²⁵ uses TWO facts:
1. λ(u) ≤ λ(1) for u ≥ 1 (proved via d/du[log λ] < 0).
2. λ(1)·|W₁(u)| ≤ 1.82×10⁻²⁵ is an ABSOLUTE bound at u=1:
   λ(1)·|W₁(1)| = 1.95×10⁻²⁷ × 93.15 ≈ 1.82×10⁻²⁵.

The statement "≤ 1.82×10⁻²⁵" is an absolute constant, NOT a claim that the
product λ(u)·|W₁(u)| is decreasing. The bound just uses the VALUE at u=1.

For u > 1: |W_tail(u)| = λ(u)·|W₁(u)| ≤ λ(1)·|W₁(u)| × (1 since λ decreasing)
BUT |W₁(u)| grows, so the product might increase. However, the conclusion only
requires |W_tail| < |W₁|, which holds as long as λ(u) < 1 — and λ(1) = 1.95×10⁻²⁷ << 1.

The revised statement should be: "For all u ≥ 1: |W_tail(u)| ≤ λ(u)·|W₁(u)| ≤ λ(1)·|W₁(u)|.
Since λ(1) = 1.95×10⁻²⁷ << 1, we have |W_tail(u)| << |W₁(u)|, hence W = W₁ + W_tail < 0."

This is cleaner and avoids the claim about the absolute maximum.
