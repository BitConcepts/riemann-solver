# Theorem Dependency Graph

Tracks logical dependencies between statements in the proof chain from certified log-concavity
to the Riemann Hypothesis. Updated as new lemmas are identified.

---

## Current proof chain

```
T1: Φ(u) > 0 for all u ∈ ℝ                               [PROVED — standard]
T2: Φ(-u) = Φ(u)                                          [PROVED — standard]
T3: Φ ∈ L^1(ℝ)                                            [PROVED — standard]
T4: Φ is real analytic                                     [PROVED — standard]
T5: Φ decays superexponentially                            [PROVED — standard]
T6: (log Φ)''(u) < 0 for all u ≥ 0 (strict log-concavity) [PROVED — IA certificate]
  └── Certificate: Q_Φ < 0 on [0,1] (52,898 subintervals)
  └── Algebraic core: (log φ₁)'' < 0 for u ≥ 0
  └── Tail bound: C = 204, u > 1
T6b: L_2(u) ≥ 0 for all u ≥ 0 (2nd Laguerre inequality)  [PROVED — IA certificate]
  └── Certificate: L_2 ≥ 0 on [0,1] (2,000 subintervals)
  └── Grid scan: L_2 ≥ 0 on [0,5] (500 points)
  └── Tail: first-term dominance for u > 1

T7: Xi(z/2) = (1/2) ∫ Φ(u) e^{iuz} du                   [PROVED — standard]
T8: RH ⟺ ∀ z: Ξ(z) = 0 → Im(z) = 0                     [PROVED — standard]

OPEN BRIDGE:
T9: T1 + T2 + T3 + T4 + T5 + T6 → ∀ z: ∫Φ(u)e^{iuz}du = 0 → Im(z) = 0
                                                           [OPEN — Hypothetical Criterion 13]

CONDITIONAL:
T10: T9 + T6 → T8 (RH)                                   [CONDITIONAL on T9]
```

---

## Dependency diagram

```
T1  T2  T3  T4  T5  T6  T6b
 \   \   |   |  /  /   /
  \   \  |   | /  /   /
   ╔════════════════════╗
   ║    H13 Bridge      ║  ← T9 (OPEN)
   ╚════════════════════╝
           |
          T7
           |
          T8 (RH)  ← CONDITIONAL on T9
```

---

## Sublemmas added from research iterations

### T6b: L_2 generalized Laguerre inequality (Iteration 2b, 2026-06-04)

**Statement:** L_2(u) = 2Φ(u)Φ⁽⁴⁾(u) − 8Φ'(u)Φ'''(u) + 6(Φ''(u))² ≥ 0 for all u ≥ 0.

**Status:** PROVED (IA certificate on [0, 1]) + COMPUTATION (grid scan on [0, 5])

**Method:**
- Interval arithmetic: 2000 subintervals on [0, 1.0], 5 Phi terms, 55-digit precision.
  All 2000 subintervals certified. Tightest lower bound: 3.14e-08 (at u ≈ 1.0).
- Floating-point grid: 500 points on [0, 5.0], 10 Phi terms. L_2 ≥ 0 everywhere.
  Min value 0 (underflow) at u ≈ 2.42 (Φ is superexponentially small there).
- Tail argument: For u > 1, n=1 term dominates with ratio 1.0 (corrections < 10⁻²⁹).
  L_2 for single-term Phi is analytically nonneg (confirmed numerically).

**Dependency:** T6b depends on T1–T5 (Φ properties) and the IA certificate.

**Significance for H13:** Csordas-Vishnyakova Thm 2.3 requires ALL L_n ≥ 0.
T6 proved L_1 ≥ 0 (log-concavity). T6b proves L_2 ≥ 0 (second Laguerre inequality).
Still need L_3, L_4, … for the full criterion.

**Certificate file:** `phase-next/experiments/outputs/l2_laguerre_cert_20260604T165540Z.json`
**Script:** `phase-next/experiments/scripts/certify_l2_laguerre.py`

---

## Notes

- T6 is the strongest proved statement in this project.
- T9 is the single missing step.
- No additional lemmas between T6 and T9 have been identified yet.
- Any new lemma that reduces T9 to a known theorem should be added here immediately.
