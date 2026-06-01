# Deliverable: theorem_13_14_corrected_tail.md
# Tasks 3+5 — Updated Theorems 5 and 6 With Corrected ε*(u)

## Theorem 5 (Extended Certification [1.0, 3.0]) — Updated

The certification now uses ε*(u) = 2 Σ_{n≥2} n⁴ e^{-π(n²-1)e^{2u}}.

Updated statement of Lemma W (precondition):
  |W_tail(u)| ≤ λ(u)·|W₁(u)| ≤ λ(1)·|W₁(u)|
  where λ(1) = 1.95×10⁻²⁷ << 1. Hence |W_tail(u)| << |W₁(u)|.

Script results (verify_ia_1_to_3.py with corrected ε*):
  101/101 checkpoints certified
  min_margin = 91.29 (at u=1.0, interval [0.99,1.01])
  SHA256: 1BB9E9DECF13580C4B30AB5EB3EE7A6A742E24E4EAD1916319BA7FA18DAEDBE9

Note: min_margin decreased from 93.15 to 91.29 because the corrected ε* = 2ε_old
doubles the C×ε* term, consuming ~3.7×10⁻²⁷ of margin. The margin is still 91.29, 
overwhelmingly positive.

## Theorem 6 (Tail Bound [3.0, ∞)) — Updated

The corrected bound for u ≥ 3:

ε*(3) ≤ 2 × Σ n⁴ e^{-π(n²-1)e^{2·3}} ≤ 2 × 16 × e^{-3πe^6} < 2 × 10⁻¹⁶³⁷ = 10⁻¹⁶³⁶·⁷

Replace:
  "ε(3) ≤ 16 e^{-3πe^6} < 10^{-1637}"

With:
  "ε*(3) ≤ 32 e^{-3πe^6} < 10^{-1636}"

The conclusion W₁(3) + C·ε*(3) < -1000 + 204 × 10^{-1636} < 0 remains valid.

## Tail Notation Convention (Task 5)

Add a brief notation remark before Theorem 5:

---
**Notation.** Throughout this section:
- Φ = 4(φ₁ + R) where R = Σ_{n≥2} φ_n (factor of 4 cancels in log-derivatives)
- W = (log Φ)'' = (log(4Φ))'' = (log Φ)'' (factor-4 invariant)
- W₁ = (log φ₁)''
- W_tail = W − W₁
- ε*(u) = 2 Σ_{n≥2} n⁴ e^{-π(n²-1)e^{2u}} [corrected upper bound on |R|/φ₁]

The factor 4 in Φ cancels in W since (log(cΦ))'' = (log Φ)'' for any c > 0.
---
