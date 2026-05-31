# Q Scaling Audit: Factor-of-4 Consistency

**Claim under audit:** The factor of 4 in Φ = 4·Σφ_n does not affect the sign of Q_Φ,
and all perturbation bounds (C=204, ε values) are computed consistently.

---

## 1. Scaling Invariance of Q

### Algebraic identity
For any constant c > 0 and function f:

Q_{cf}(u) = (cf)''(cf) - ((cf)')² = c²(f''f - (f')²) = c² · Q_f(u)

Since c² > 0, sign(Q_{cf}) = sign(Q_f). ∎

### Application to Φ = 4·Σφ_n
With c = 4 and f = Σφ_n = φ₁ + R:

Q_Φ = 16 · Q_{φ₁+R} = 16 · (Q_{φ₁} + ΔQ)

The factor 16 is positive, so Q_Φ < 0 ⟺ Q_{φ₁} + ΔQ < 0 ⟺ |ΔQ| < |Q_{φ₁}|.

**Verdict:** Scaling by 4 is algebraically irrelevant to the sign determination. ✓

## 2. Definition of R in the Paper

From paper Section 6 (Theorem 5), equation for ΔQ:

> "Write Q_Φ = Q_{φ₁} + ΔQ where
>  ΔQ = φ₁''R + R''φ₁ + R''R − 2φ₁'R' − (R')²"

This uses φ₁ and R = Σ_{n≥2} φ_n **without** the factor of 4. The paper works at the
level of the inner sum (φ₁ + R), not Φ = 4(φ₁ + R).

**Consistency check:** Since Q_Φ = 16·Q_{φ₁+R}, the paper correctly factors out the 16
and proves Q_{φ₁+R} < 0 directly. The ε and C values are computed from φ₁ and R (no factor 4).

## 3. Code Audit: verify_algebraic_core.py (Attack 7)

From `proof/verify_algebraic_core.py`, lines 91-114:

```python
phi1, phi1p, phi1pp = get_derivs(1, 1, u)   # n=1 only, NO factor 4
R, Rp, Rpp = get_derivs(2, 20, u)           # n=2..20, NO factor 4

eps_R = float(abs(R) / abs(phi1))            # ratio within inner sum
Q_phi1 = phi1pp * phi1 - phi1p**2            # Q of phi1 alone (no factor 4)
Delta_Q_actual = (phi1pp*R + Rpp*phi1 + Rpp*R - 2*phi1p*Rp - Rp**2)
```

The code computes φ₁, R without factor 4. The Q_{φ₁} is φ₁''φ₁ − (φ₁')² (no factor 4).
ΔQ is computed from the same unscaled quantities.

**Verdict:** Code uses inner-sum quantities consistently. ✓

## 4. Code Audit: falsify_advanced.py (Attack 7)

From `falsification/falsify_advanced.py`, lines 106-131:

Same `get_derivs` function, same pattern: φ₁ and R computed without factor 4.
Line 131: `implied_C = exact_ratio / eps_R` computes C from the unscaled quantities.

The function `Phi(u, N=20)` at line 28 does include the factor 4:
```python
def Phi(u, N=20):
    return 4*sum(phi_n(n, u) for n in range(1, N+1))
```
This is used for the convention check (Attack 6), where it computes ∫Φ(u)du = ξ(1/2).
The convention check uses the full Φ (with factor 4) to match against ξ(1/2). ✓

**Verdict:** Attack 7 uses inner-sum quantities for C, Attack 6 uses full Φ for ξ matching. Both correct. ✓

## 5. Code Audit: verify_logconcavity_rigorous.py

From `proof/verify_logconcavity_rigorous.py`, lines 73-85:

```python
def Phi_and_derivs_iv(u_iv):
    for n in range(1, N_TERMS + 1):
        f, fp, fpp = phi_n_and_derivs_iv(n, u_iv)
        f_total += f; fp_total += fp; fpp_total += fpp
    return 4 * f_total, 4 * fp_total, 4 * fpp_total
```

This returns Φ = 4·Σφ_n, Φ' = 4·Σφ_n', Φ'' = 4·Σφ_n''.

Then Q_Phi_rigorous (line 99): `Q = fpp * f - fp ** 2`

This computes Q_Φ = Φ''Φ − (Φ')² = (4·Σφ_n'')(4·Σφ_n) − (4·Σφ_n')²
= 16·(Σφ_n''·Σφ_n − (Σφ_n')²) = 16·Q_{φ₁+R}

The IA verification checks Q_Φ < 0, which is equivalent to Q_{φ₁+R} < 0.

**Verdict:** IA verification uses full Φ (with factor 4). Sign is preserved by 16× scaling. ✓

## 6. Verification of C = 204

### Numerical recomputation
From `compute_lambda_tail.py` output (300-digit precision, 30 terms):

At u = 1.0:
- ε = |R|/φ₁ = 9.5873 × 10⁻³⁰
- Q_{φ₁} = −1.7683 × 10⁻¹²
- ΔQ = 3.4515 × 10⁻³⁹
- λ = |ΔQ|/|Q_{φ₁}| = 1.9518 × 10⁻²⁷
- C = λ/ε = 203.6

Paper states: C = 204, ε = 9.59 × 10⁻³⁰, λ = 1.95 × 10⁻²⁷.

**Verdict:** C = 204 is the ceiling of 203.6 (rounded up for safety). Values match to stated precision. ✓

### Consistency of ε values
Paper states ε(1.0) = 9.59 × 10⁻³⁰, ε(1.5) = 9.98 × 10⁻⁸², ε(2.0) = 5.37 × 10⁻²²³.

Computed: ε(1.0) = 9.5873e-30, ε(1.5) = 9.9835e-82, ε(2.0) = 5.3667e-223.

All match to 3+ significant figures. ✓

## 7. Cross-Layer Consistency

The proof has three layers:

1. **IA layer** (verify_logconcavity_rigorous.py): Uses Φ = 4·Σφ_n (5 terms), checks Q_Φ < 0
2. **Truncation layer** (verify_truncation_and_crosscheck.py): Bounds |4·Σ_{n≥6}φ_n| on [0,1]
3. **Perturbation layer** (verify_algebraic_core.py): Uses φ₁, R without factor 4

Layer 1 computes Q_{Φ_5} where Φ_5 = 4·Σ_{n=1}^{5}φ_n. The factor 4 is applied.
Layer 2 bounds δ = 4·Σ_{n≥6}φ_n. The factor 4 is applied.
Layer 3 bounds |ΔQ|/|Q_{φ₁}| using unscaled φ₁, R. Factor 4 is NOT applied (correctly, since
Q_Φ = 16·Q_{φ₁+R} and 16 doesn't change the sign).

The paper's proof for u ∈ [0,1] uses layers 1+2 (Q_Φ directly).
The paper's proof for u > 1 uses layer 3 (Q_{φ₁+R} via perturbation).
The two are compatible because Q_Φ = 16·Q_{φ₁+R}.

## 8. Potential Ambiguity in R Definition

One subtlety: the paper defines R = Σ_{n≥2}φ_n (Section 5, Proposition 5):
"where R = Σ_{n≥2}φ_n"

This is consistent with Φ = 4(φ₁ + R) = 4φ₁ + 4R. The factor 4 multiplies the entire sum.
The truncation bound in Remark 4 defines δ = 4·Σ_{n≥6}φ_n, which correctly includes the factor 4.

There is NO ambiguity: R is always the inner sum (without factor 4) in the perturbation analysis.

## 9. Gaps Found

### No scaling errors found.

The factor-of-4 treatment is consistent across all code and paper sections:
- Q_Φ = 16·Q_{φ₁+R} (algebraically correct)
- IA verification uses full Φ (factor 4 included)
- Perturbation bound uses inner sum (factor 4 factored out)
- C = 204 is correctly computed from unscaled quantities
- ε values match between paper and code to 3+ significant figures

### Minor observation
The paper could be more explicit about the factorization Q_Φ = 16·Q_{φ₁+R} in Theorem 5.
Currently it jumps from "Write Q_Φ = Q_{φ₁} + ΔQ" without stating that this is actually
Q_{φ₁+R} = Q_{φ₁} + ΔQ (at the inner-sum level, not the Φ level). A careful reader might
wonder whether Q_Φ = Q_{φ₁} + ΔQ or Q_Φ = 16·(Q_{φ₁} + ΔQ). The paper should state the
factorization explicitly.

**Impact:** This is a presentation issue, not a mathematical error. The formula for ΔQ
(in terms of φ₁, R without factor 4) is correct regardless.

## 10. Verdict

**SCALING CONSISTENT**

All factor-of-4 handling is correct. R is defined as Σ_{n≥2}φ_n (without factor 4)
throughout the perturbation analysis. The IA verification uses the full Φ = 4·Σφ_n.
C = 204 and all ε values are computed consistently. No scaling errors found.
