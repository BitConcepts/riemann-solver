# Deliverable: epsilon_star_notation_cleanup.md — ε* Notation Consistency

## Problem
Theorem 5 proof uses ε and ε* interchangeably. The ε definition says
|W_tail| ≤ C·ε(u) then immediately redefines ε*(u) = 2Σn⁴... The
bracket [corrected: B_n(u)/n^4 < 2] appears inside displayed math.

## Required changes

1. Define ε*(u) once in Proposition 5, not inline in a displayed equation.
2. In Theorem 5 proof: use only ε*(u) throughout. Drop all ε references.
3. C definition: "C = |ΔQ|/(ε*(1)·|Q_φ₁(1)|)" with ε*(1) = 1.82×10⁻²⁹.
   Note: C* ≈ 112 ≤ 204, so using C=204 with ε* is conservative.
4. Remove editorial note from inside math.
5. In Theorem 6: replace all ε(u) with ε*(u) consistently.
6. "Tail ratios" in Theorem 6: label as ε*(1.0), ε*(1.5), etc.

## Old ε values (uncorrected, for reference only)
ε_old(1.0) = 9.59×10⁻³⁰  [no longer used in proof]
ε_old(1.5) = 9.98×10⁻⁸²  [no longer used in proof]

## Corrected ε* values (twice the old ε)
ε*(1.0) ≈ 1.82×10⁻²⁹  [= 2 × 9.115×10⁻³⁰, computed]
ε*(1.5) ≈ 1.96×10⁻⁸¹  [= 2 × 9.804×10⁻⁸²]
ε*(2.0) ≈ 1.07×10⁻²²²  [= 2 × 5.33×10⁻²²³]
ε*(3.0) ≤ 32e^{-3πe^6} < 10^{-1636}  [= 2 × 16e^{-3πe^6}]
