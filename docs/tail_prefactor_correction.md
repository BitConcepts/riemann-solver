# Deliverable: tail_prefactor_correction.md
# Task 1 — Audit and Fix Proposition 5 / ε(u) Tail Prefactor Bound

## 1. The Problem: n⁴ Is Not a Valid Upper Bound

The paper's Proposition 5 claims |φ_n|/φ₁ ≤ n⁴ e^{-π(n²-1)e^{2u}}. This is false.

### Exact derivation of B_n(u)

Factor both terms:
  φ_n(u) = π n² e^{5u/2} · h_n(u) · e^{-πn²e^{2u}},  h_n = 2πn²e^{2u} − 3
  φ_1(u) = π e^{5u/2}     · h_1(u) · e^{-πe^{2u}},    h_1 = 2πe^{2u} − 3

Therefore:
  |φ_n(u)| / φ_1(u) = [n² · h_n(u) / h_1(u)] · e^{-π(n²-1)e^{2u}} =: B_n(u) · e^{-π(n²-1)e^{2u}}

where B_n(u) = n² (2πn²e^{2u} - 3) / (2πe^{2u} - 3).

### Proof that the old n⁴ bound is invalid

We need: B_n(u) ≤ n⁴?
  B_n ≤ n⁴  ⟺  n²h_n ≤ n⁴h_1  ⟺  h_n ≤ n²h_1
  ⟺  2πn²e^{2u} - 3 ≤ n²(2πe^{2u} - 3)
  ⟺  -3 ≤ -3n²  ⟺  n² ≤ 1.

This fails for all n ≥ 2. The n⁴ bound is **strictly invalid** as an upper bound.

## 2. Numerical Evidence

Computed values (50-digit precision):

  B_n(u)/n⁴ at u=0: n=2 → 1.6853, n=3 → 1.8122, n=4 → 1.8566 (INVALID)
  B_n(u)/n⁴ at u=1: n=2 → 1.0518, n=3 → 1.0614, n=4 → 1.0648 (INVALID)
  B_n(u)/n⁴ at u=3: n=2 → 1.0009, n=3 → 1.0011, n=4 → 1.0011 (INVALID)

The ratio B_n/n⁴ → 1 as u → ∞ but exceeds 1 for all finite u.

## 3. Corrected ε*(u)

### Option A: Exact bound

  ε*(u) = Σ_{n≥2} B_n(u) · e^{-π(n²-1)e^{2u}}

### Option B: Conservative global bound (recommended for paper clarity)

Since B_n(u)/n⁴ ≤ 1 + 3/(2π-3) < 1.915 < 2 for all u ≥ 0, n ≥ 2:

  ε*(u) = 2 · Σ_{n≥2} n⁴ · e^{-π(n²-1)e^{2u}} = 2 ε_old(u)

This is a clean, valid upper bound.

## 4. Updated Numerical Values

Using the exact B_n(u) formula:
  ε*(1.0) = 9.587×10⁻³⁰   [vs ε_old(1.0) = 9.115×10⁻³⁰, ratio 1.052]
  ε*(1.5) = 9.984×10⁻⁸²   [vs ε_old(1.5) = 9.804×10⁻⁸², ratio 1.018]
  ε*(2.0) = 5.367×10⁻²²³  [vs ε_old(2.0) = 5.331×10⁻²²³, ratio 1.007]
  ε*(3.0) ≈ 10⁻¹⁶³⁷ (essentially unaffected, correction factor ≈ 1.0009)

Using the factor-2 conservative bound (simpler):
  ε*(1.0) = 1.823×10⁻²⁹   [vs ε_old(1.0) = 9.115×10⁻³⁰]
  These are 2× larger than the old values.

## 5. Updated Proposition 5

Replace:
> "Each |φ_n|/φ_1 ≤ n⁴ e^{-π(n²-1)e^{2u}} by Lemma (tail_decay).
>  At u=0: Σ n⁴ e^{-π(n²-1)} < 16e^{-3π} + 81e^{-8π} + ⋯ < 0.003."

With:
> "Each |φ_n|/φ_1 = B_n(u) e^{-π(n²-1)e^{2u}} where B_n(u) = n²h_n/h_1 ≤ 2n⁴
>  (since B_n/n⁴ ≤ 1 + 3/(2π-3) < 2 for all u ≥ 0).
>  At u=0 (worst case): Σ 2n⁴ e^{-π(n²-1)} < 32e^{-3π} + 162e^{-8π} + ⋯ < 0.006 < 1/50."

## 6. Updated Lemma W

Lemma W remains valid. The update:
  |W_tail(u)| ≤ λ(1)·|W_1(u)| ≤ 1.82×10⁻²⁵

This bound was derived from the actual λ(u) = |ΔQ|/|Q_φ₁| which does NOT depend on the ε definition. It remains valid.

However, the NARRATIVE in Theorems 5-6 that presented the ε-based reasoning should be updated to use the corrected ε* to avoid the impression that the invalid n⁴ bound was used.

## 7. C=204 Audit Under Corrected ε*

C was defined as C = |ΔQ|/(ε × |Q_φ₁|)|_{u=1} = 204, using ε_old(1) = 9.115×10⁻³⁰.

Under the corrected ε*(1) = 9.587×10⁻³⁰ (exact B_n formula):
  C* = |ΔQ|/(ε* × |Q_φ₁|)|_{u=1} = 204 × (9.115/9.587) ≈ 194

C* < C = 204, so using C = 204 with ε* is conservative. No change needed to the constant.

For the factor-2 bound (ε* = 2ε_old): C* = 204/2 = 102.

## 8. Confirmation: All Margins Remain Valid

The key quantity at each checkpoint is: margin = |W_1(I_i)| - C×ε*(I_i)

At u=1.0 (worst case):
  Old margin: 93.15 - 204×9.115×10⁻³⁰ ≈ 93.15 - 1.86×10⁻²⁷ ≈ 93.15
  Corrected (using 2×): 93.15 - 204×2×9.115×10⁻³⁰ ≈ 93.15 - 3.72×10⁻²⁷ ≈ 93.15

The correction is at the level of 10⁻²⁷ relative to a margin of 93.15. **All conclusions unchanged.**

## Acceptance Criterion

✓ Invalid n⁴ bound identified and corrected to 2n⁴ (or exact B_n).
✓ All numerical values updated.
✓ All theorems and propositions remain valid (correction is < 5% at u=1, < 0.1% at u=3).
✓ C=204 remains conservative under corrected ε*.
