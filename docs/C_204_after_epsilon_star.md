# Deliverable: C_204_after_epsilon_star.md — C=204 Audit

## Current state
C = |ΔQ(1)|/(ε_old(1)·|Q_φ₁(1)|) = 204  [using old ε]

## Under corrected ε*(1) ≈ 1.82×10⁻²⁹ (= 2 × ε_old(1)):
C* = |ΔQ(1)|/(ε*(1)·|Q_φ₁(1)|) = 204/(1.82×10⁻²⁹/9.115×10⁻³⁰) = 204/2.0 ≈ 102

Since C* ≈ 102 < 204: using C=204 with ε* is conservative.

## Paper text (add after C definition):
"Since ε*(1) = 2ε_old(1), we have C* = C/2 ≈ 102. Using C=204 with ε* 
is conservative: C·ε* = 204·ε* ≥ 2C*·ε* ≥ C*·ε* while C·ε* is doubly-
exponentially small (≈ 3.7×10⁻²⁷ at u=1, vs margin 91.3)."
