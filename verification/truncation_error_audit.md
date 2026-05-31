# Truncation Error Audit

**Auditor:** Oz (automated verification agent)
**Date:** 2026-05-31
**Status:** Verified with caveats; error propagation analysis reveals the paper's claim is safe but imprecisely stated

---

## 1. What Does 7.03×10⁻⁴³ Bound?

The paper claims "truncation error < 7.03×10⁻⁴³ from omitting n ≥ 6."

**Precisely:** This bounds the maximum of |4·Σ_{n≥6} φ_n(u)| over u ∈ [0, 1].

This is a bound on the **value** of the omitted terms in Φ. It does NOT directly bound:
- The omitted contribution to Φ'
- The omitted contribution to Φ''
- The error in Q_Φ = Φ''Φ − (Φ')²

The script `verify_truncation_and_crosscheck.py` (lines 30–62) computes this bound using interval arithmetic, summing |4·φ_n| upper bounds for n = 6..19, plus a tail bound for n ≥ 20.

---

## 2. Verification of the 7.03×10⁻⁴³ Bound

**Individual term bounds** (interval arithmetic, 60-digit precision):

```
n =  6: |4·φ_n| ≤ 7.0270e-43   (dominates)
n =  7: |4·φ_n| ≤ 2.3860e-60
n =  8: |4·φ_n| ≤ 1.3931e-80
n =  9: |4·φ_n| ≤ 1.4263e-103
n = 10: |4·φ_n| ≤ 2.5947e-129
n = 11: |4·φ_n| ≤ 8.4673e-158
n = 12: |4·φ_n| ≤ 4.9917e-189
n = 13: |4·φ_n| ≤ 5.3442e-223
n = 14: |4·φ_n| ≤ 1.0434e-259
n = 15: |4·φ_n| ≤ 3.7274e-299
n ≥ 16: underflows to 0 in 60-digit arithmetic
```

**Total:** 7.0270×10⁻⁴³ ✓

The bound is overwhelmingly dominated by the n = 6 term. Each subsequent term is at least 17 orders of magnitude smaller.

**Bound method:** For u ∈ [0, 1], the bound uses:
- |g_n(u)| ≤ 2π²n⁴e^{9/2} (since e^{9u/2} ≤ e^{9/2} for u ≤ 1)
- E_n(u) ≤ e^{−πn²} (since e^{2u} ≥ 1 for u ≥ 0, so e^{−πn²e^{2u}} ≤ e^{−πn²})

This gives an upper bound of 4·2π²n⁴e^{9/2}·e^{−πn²} per term. The bound is valid but not tight: at u = 0 the actual value is smaller because the subtracted term 3πn²e^{5u/2} is nonzero.

---

## 3. Derivative Truncation Bounds

The paper does NOT explicitly state bounds on the omitted Φ' and Φ'' contributions. I computed them:

```
δ   = |4·Σ_{n≥6} φ_n(u)|   ≤ 7.03×10⁻⁴³   (the stated bound)
δ'  = |4·Σ_{n≥6} φ_n'(u)|  ≤ 1.18×10⁻³⁹   (computed, not in paper)
δ'' = |4·Σ_{n≥6} φ_n''(u)| ≤ 1.98×10⁻³⁶   (computed, not in paper)
```

The derivative bounds are larger because differentiation introduces polynomial factors (up to π²n⁴e^{4u}), but still utterly negligible compared to the Q_Φ margin.

---

## 4. Error Propagation Through Q_Φ

The IA verification computes Q_Φ using N = 5 terms:

```
Φ_5 = 4·Σ_{n=1}^{5} φ_n    (computed)
Φ   = Φ_5 + δ               (true value, where δ = 4·Σ_{n≥6} φ_n)
```

The computed log-concavity numerator is:

```
Q_{Φ_5} = Φ_5'' · Φ_5 − (Φ_5')²
```

The true value is:

```
Q_Φ = (Φ_5'' + δ'')(Φ_5 + δ) − (Φ_5' + δ')²
    = Q_{Φ_5} + [Φ_5''·δ + δ''·Φ_5 − 2·Φ_5'·δ'] + [δ''·δ − (δ')²]
```

The error has:
- **Linear (cross) terms:** Φ_5''·δ + δ''·Φ_5 − 2·Φ_5'·δ'
- **Quadratic terms:** δ''·δ − (δ')²

### Explicit error at u = 1 (worst case for margin):

```
At u = 1 with N = 5:
  Φ_5    = 5.511e-07
  Φ_5'   = −2.303e-05
  Φ_5''  = 9.111e-04

Error terms in Q:
  |Φ_5'' · δ|    = 6.405e-46
  |δ'' · Φ_5|    = 1.091e-42   ← dominant cross term
  2|Φ_5' · δ'|   = 5.435e-44
  |δ'' · δ|      = 1.392e-78   (negligible quadratic)
  |δ' ²|         = 1.392e-78   (negligible quadratic)

  Total error bound = 1.146e-42
```

### At u = 1:

```
|Q_Φ|          = 2.829e-11
Error / |Q_Φ|  = 4.051e-32
Safety factor  = 2.468e+31
```

### At u = 0:

```
|Q_Φ|          = 5.979e+01
Error          = 3.538e-36
Safety factor  = 1.690e+37
```

---

## 5. Is the Error Propagation Correctly Handled?

### What the paper claims (Section 5, Remark)

> "The truncation error from omitting terms n ≥ 6 in the interval arithmetic computation is bounded rigorously by 7.03 × 10⁻⁴³ over [0,1]. Since |Q_Φ(u)| ≥ 3.36 × 10⁻¹² on this interval, the truncation error is 10³⁰ times smaller than the certified margin and cannot affect any sign determination."

### What's actually true

The 7.03×10⁻⁴³ bounds the omitted Φ terms, not the error in Q_Φ. The error in Q_Φ involves cross terms with Φ'' and Φ, which amplify the truncation error. However:

- The **actual** error in Q is bounded by ~1.15×10⁻⁴² (computed above)
- The margin is 3.36×10⁻¹² (from IA verification)
- The safety factor is ~2.9×10³⁰

The paper's claim of "10³⁰ times smaller" is approximately correct (actual: ~2.9×10³⁰ at the worst point), but the reasoning is imprecise:

**The paper compares δ (truncation in Φ) directly to |Q_Φ| (the margin in the quadratic form).** This is dimensionally inconsistent — δ has units of Φ while Q has units of Φ². The correct comparison is δ_Q (error in Q) vs |Q_Φ|.

Fortunately, the error amplification factor |Φ''|/|Φ| ≈ 9.1e-4/5.5e-7 ≈ 1655 at u = 1. So the actual Q error is δ·|Φ''| ≈ 7e-43 · 1.7e3 ≈ 1.2e-39, still vastly smaller than 3.36e-12.

**Bottom line:** The conclusion is correct but the stated reasoning skips the error propagation step.

---

## 6. Safety Factor Analysis

The minimum margin (max upper bound on Q from IA) is −3.36×10⁻¹² at the worst subinterval near u ≈ 0.9999.

```
Safety factor = |margin| / |error in Q|
             = 3.36e-12 / 1.15e-42
             ≈ 2.9 × 10³⁰
```

This is an enormous safety margin. The truncation error would need to be amplified by a factor of 10³⁰ to affect any sign determination. Even accounting for potential error in the bounds themselves (e.g., rounding in interval arithmetic), the margin is many orders of magnitude beyond any conceivable numerical issue.

---

## 7. Cross-Validation

The script `verify_truncation_and_crosscheck.py` (Part 2) cross-validates Q_Φ values computed via:
- **Method A:** Interval arithmetic (mpmath.iv) at 60-digit precision
- **Method B:** High-precision floating point (mpmath) at 80-digit precision

At 10 selected points on [0, 1], all floating-point Q values lie within the corresponding IA enclosures. This confirms that the interval arithmetic is computing correctly and that the enclosures are not spuriously wide.

---

## 8. Identified Gaps

### GAP 1: Paper conflates truncation error in Φ with error in Q_Φ

The paper states the truncation bound is 7.03×10⁻⁴³ and compares it to the Q margin of 3.36×10⁻¹², claiming a 10³⁰ safety factor. This is dimensionally incorrect: the truncation error in Φ must be propagated through Q = Φ''Φ − (Φ')² to obtain the error in Q.

**Impact:** None on validity. The actual error in Q is ~1.15×10⁻⁴², and the safety factor is ~2.9×10³⁰ — essentially the same conclusion. The paper's reasoning is imprecise but the conclusion holds.

### GAP 2: Derivative truncation bounds not stated

The paper does not explicitly bound |δ'| or |δ''|. These are needed for rigorous error propagation but are implicitly handled by the interval arithmetic (which uses N = 5 terms for all three of Φ, Φ', Φ'').

**Impact:** Low. The IA computation includes all terms n = 1..5 for all derivatives, so the truncation error in each derivative is bounded by the omitted n ≥ 6 terms. The bounds computed above (δ' ≤ 1.18×10⁻³⁹, δ'' ≤ 1.98×10⁻³⁶) are adequate.

### GAP 3: The IA enclosure already accounts for truncation

A subtle point: the IA verification computes Q for Φ_5 (the 5-term partial sum), not for the true Φ. If Q_{Φ_5} < 0 on all subintervals AND the truncation error in Q is small compared to the margin, then Q_Φ < 0 follows.

This is exactly what happens. The IA certifies Q_{Φ_5} < −3.36×10⁻¹² on all subintervals, and the truncation error contributes at most ~10⁻⁴² to Q, so Q_Φ < −3.36×10⁻¹² + 10⁻⁴² < 0.

**Impact:** None. The logic is sound, just not explicitly spelled out in the paper.

---

## 9. Verdict

The truncation error analysis is **safe** but **imprecisely stated** in the paper. The 7.03×10⁻⁴³ bound is correct for |δ| = |4·Σ_{n≥6} φ_n|. The propagated error in Q_Φ is ~1.15×10⁻⁴², which is 2.9×10³⁰ times smaller than the IA margin. The conclusion (truncation cannot affect sign determination) is correct.

The paper would be strengthened by:
1. Stating that 7.03×10⁻⁴³ bounds δ (the value), not the error in Q
2. Noting that Q_Φ = Q_{Φ_5} + O(δ·|Φ''|) and computing this explicitly
3. Stating the derivative truncation bounds δ' and δ''

None of these are proof-breaking gaps.
