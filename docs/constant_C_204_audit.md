# Deliverable: constant_C_204_audit.md
# Task 4 — C = 204 Constant Audit Under Corrected ε*(u)

## Summary: C = 204 REMAINS CONSERVATIVE

C was defined as: C = |ΔQ(1)| / (ε(1) × |Q_φ₁(1)|) = 204

Using ε_old(1) = 9.115×10⁻³⁰.

Under the corrected ε*(1) = 9.587×10⁻³⁰ (exact B_n formula):
  C* = |ΔQ(1)| / (ε*(1) × |Q_φ₁(1)|) = 204 × (9.115/9.587) ≈ **194**

Since C* < C = 204, using C = 204 with ε* is conservative.
The paper may continue to use C = 204.

Alternatively, with the factor-2 bound (ε* = 2ε_old):
  C* = 204/2 = 102

In this case, C* × ε* = 102 × 2ε_old = 204 × ε_old — the product is the same.
So using C = 204 with ε* = 2ε_old is equivalent to using C = 102 with ε_old.

## Recommended presentation

To avoid confusion, the paper should state clearly:

"We use ε*(u) = 2 Σ_{n≥2} n⁴ e^{-π(n²-1)e^{2u}} as a valid upper bound on |R|/φ₁
(see Proposition 5). The corresponding constant at u=1 is C* = |ΔQ|/(ε*·|Q_φ₁|)|_{u=1}
= 102 ≤ 204, so using C = 204 remains conservative."

## Impact on Theorem 5 certification

The script now certifies: W₁(I_i) + 204 × ε*(I_i) < 0
where ε* = 2ε_old. The minimum margin became 91.29 (vs 93.15 before).
Both values are overwhelmingly positive; all 101 checkpoints certified.
