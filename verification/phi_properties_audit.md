# Φ Properties Audit

**Auditor:** Oz (automated verification agent)
**Date:** 2026-05-31
**Status:** PHI PROPERTIES VERIFIED (all five Pólya conditions satisfied)

---

## 1. Overview

The paper's Corollary 8 (RH) invokes Pólya's theorem (Theorem 1) with K = Φ. The theorem requires six conditions: (i) positivity, (ii) evenness, (iii) integrability, (iv) log-concavity, (v) superexponential decay, (vi) real analyticity near the origin. This audit verifies conditions (i), (ii), (iii), (v), and (vi). Condition (iv) is the subject of the IA verification and perturbation bound, audited elsewhere.

The kernel is:
```
Φ(u) = 4 Σ_{n=1}^∞ φₙ(u),   φₙ(u) = (2π²n⁴e^{9u/2} − 3πn²e^{5u/2}) e^{−πn²e^{2u}}
```

---

## 2. Condition (i): Φ(u) > 0 for all u

### For u ≥ 0: Term-by-term positivity

Factor each term:
```
φₙ(u) = πn²e^{5u/2} · (2πn²e^{2u} − 3) · e^{−πn²e^{2u}}
```

The three factors:
- πn²e^{5u/2} > 0 always ✓
- e^{−πn²e^{2u}} > 0 always ✓
- (2πn²e^{2u} − 3): for n ≥ 1 and u ≥ 0, this is ≥ 2π·1²·1 − 3 = 2π − 3 ≈ 3.28 > 0 ✓

Therefore φₙ(u) > 0 for all n ≥ 1, u ≥ 0. Since Φ = 4Σφₙ with all terms positive:

**Φ(u) > 0 for all u ≥ 0.** ✓

This is a purely algebraic argument depending only on the fact 2π > 3.

### For u < 0: Via evenness

For u < 0, individual terms φₙ(u) may be negative (when 2πn²e^{2u} < 3, which happens for u sufficiently negative). However, Φ(−u) = Φ(u) by the evenness property (condition (ii)), so Φ(u) > 0 for all u < 0 as well.

**Key dependency:** Positivity for u < 0 relies on evenness, which relies on the Jacobi theta functional equation (a deep result, not elementary).

### Margin at the worst point

At u = 1 (the worst point on [0, 1]): Φ(1) ≈ 5.51 × 10⁻⁷ (from paper's numerical check).
At u = 0: Φ(0) ≈ 1.787 (well away from zero).

**Verdict:** ✅ VERIFIED. The argument is elementary for u ≥ 0 and classical for u < 0.

---

## 3. Condition (ii): Φ(−u) = Φ(u) (Evenness)

### Source

The evenness of Φ follows from the Jacobi theta functional equation:
```
θ(1/x) = √x · θ(x),   where θ(x) = Σ_{n=−∞}^∞ e^{−πn²x}
```

This is proved via Poisson summation (a theorem, not a conjecture). The derivation from θ to Φ is standard:
- H(y) is defined from θ via differentiation (Edwards §10.3)
- The theta functional equation implies yH(y) = H(1/y)
- Under y = e^u: Φ(u) = 2e^u H(e^u) satisfies Φ(−u) = Φ(u)

### Adversarial check: Is evenness visible term-by-term?

**NO.** Each φₙ(u) is NOT individually even in u. The expression (2π²n⁴e^{9u/2} − 3πn²e^{5u/2})e^{−πn²e^{2u}} has no obvious symmetry under u → −u. The evenness is a NON-TRIVIAL property of the full sum, arising from the modular symmetry of the theta function.

### Numerical confirmation

The paper verifies |Φ(u) − Φ(−u)|/|Φ(u)| < 10⁻⁷⁰ at 8 test points. This is a consistency check, not a proof. The proof is the theta functional equation.

**Verdict:** ✅ VERIFIED. Classical result from Poisson summation; no gap.

---

## 4. Condition (iii): Φ ∈ L¹(ℝ)

### Decay analysis

For u > 0, the dominant term in Φ is φ₁(u), which contains the factor e^{−πe^{2u}}. This decays super-exponentially:
```
e^{−πe^{2u}} ≤ e^{−πe^{2}} ≈ e^{−23.1} ≈ 10⁻¹⁰   at u = 1
e^{−πe^{2u}} ≤ e^{−πe^{4}} ≈ e^{−171.5} ≈ 10⁻⁷⁵   at u = 2
```

The growth factors (e^{9u/2}, n⁴, etc.) are polynomial-exponential and are completely dominated by the super-exponential decay.

For u < 0: By evenness, Φ(u) = Φ(−u), so the same decay applies.

Therefore ∫_{−∞}^∞ |Φ(u)| du < ∞ — in fact, the integral converges extremely rapidly.

### Numerical value

∫₀^∞ Φ(u) du = ξ(1/2) ≈ 0.4971 (verified to 15 digits, Attack #6). This follows from Ξ(0) = ξ(1/2) and Ξ(0) = ∫₀^∞ Φ(u)cos(0)du = ∫₀^∞ Φ(u)du.

**Verdict:** ✅ VERIFIED. Trivially satisfied due to super-exponential decay.

---

## 5. Condition (v): Φ(u) = O(e^{−|u|^{2+δ}}) for some δ > 0

### Claimed decay

Φ(u) = O(e^{−πe^{2u}}) as u → +∞.

### Why this satisfies (v) with ANY δ > 0

For any fixed δ > 0 and large u:
```
πe^{2u} ≫ |u|^{2+δ}
```
because the exponential e^{2u} grows faster than any power |u|^N. Formally: lim_{u→∞} |u|^{2+δ} / e^{2u} = 0 by L'Hôpital. Therefore:
```
e^{−πe^{2u}} = o(e^{−|u|^{2+δ}}) for ANY δ > 0
```

The paper's Remark notes the margin at u = 8 exceeds 10^{12,000,000}. This is correct: πe^{16} ≈ 2.8 × 10⁷, while 8^{2+δ} is at most a few hundred for reasonable δ.

**Verdict:** ✅ VERIFIED. Φ exceeds the decay requirement by an astronomically large margin.

---

## 6. Condition (vi): Φ is real analytic near the origin

### Paper's claim (Corollary 8, item (vi))

"Φ is real analytic on ℝ (uniformly convergent series of analytic functions)."

### Verification

Each φₙ(u) = (2π²n⁴e^{9u/2} − 3πn²e^{5u/2}) · e^{−πn²e^{2u}} is a composition of exponentials and polynomials, hence real analytic on all of ℝ.

The series Φ(u) = 4Σ_{n=1}^∞ φₙ(u) converges uniformly on compact subsets of ℝ:
- On any compact set K ⊂ ℝ, let M = max_{u ∈ K} |u|.
- For n ≥ 2: |φₙ(u)| ≤ C·n⁴·e^{9M/2}·e^{−πn²} (using e^{2u} ≥ 1 for u ≥ 0 and evenness for u < 0).
- The sum Σn⁴e^{−πn²} converges (comparison with integral or ratio test: e^{−π(n+1)²}/e^{−πn²} = e^{−π(2n+1)} → 0).

By the theorem that a uniformly convergent series of analytic functions on compact sets is analytic, Φ is real analytic on all of ℝ.

### Why this matters: The e^{−|t|³} counterexample

The function e^{−|t|³} satisfies conditions (i)–(v) but is NOT real analytic at t = 0 (|t|³ is C^∞ but not analytic — its Taylor series at 0 is identically 0, but |t|³ ≠ 0 for t ≠ 0). Its Fourier cosine transform has infinitely many non-real zeros (Csordas-Varga Example 2.1).

The paper correctly identifies this counterexample and includes condition (vi) in Theorem 1. The earlier `polya_theorem_red_alert_audit.md` documents the discovery that the original 4-condition version was misstated.

### Subtle point: Analyticity of the even extension

Φ is defined by the series for u ≥ 0, and extended to u < 0 by Φ(−u) = Φ(u). Is the even extension analytic at u = 0?

Yes: the series converges uniformly on a neighborhood of u = 0 (say [−1, 1]) and defines an analytic function there. The even extension agrees with this analytic function (by the theta functional equation). Alternatively: each φₙ composed with |u| would NOT be analytic, but Φ is defined as the sum of the series at all u (not via |u|), and the theta functional equation provides the analytic continuation.

**Verdict:** ✅ VERIFIED. Φ is real analytic on all of ℝ by uniform convergence of analytic terms.

---

## 7. Cross-Cutting Concerns

### 7a. Does the formula define Φ for u ≥ 0 only?

The series Φ(u) = 4Σφₙ(u) converges for all u ∈ ℝ, not just u ≥ 0. For u < 0, the terms φₙ(u) are well-defined (exponentials are defined everywhere). However, the proof of positivity for u < 0 requires evenness (since individual terms may be negative).

The paper's Proposition 3 states properties for "all u ≥ 0" (item (i)) and "all u" (item (ii)). This is correct: positivity is proved for u ≥ 0 directly, and extended to u < 0 via evenness.

### 7b. Smoothness of Φ

(log Φ)″ requires Φ ∈ C². In fact, Φ is C^∞ (and even real analytic). This follows from the same uniform convergence argument used for analyticity: the series of derivatives Φ^{(k)} = 4Σφₙ^{(k)} also converges uniformly on compact sets (the exponential decay factor e^{−πn²e^{2u}} dominates any polynomial growth from differentiation).

### 7c. The paper claims "classical" for (i)–(iii) without proof

Proposition 3 says "Properties (i)–(iii) are classical; see Titchmarsh §2.10 and Csordas–Varga Theorem A." This is a valid citation strategy — these are well-established results in the literature. The term-by-term positivity proof (2π > 3) is elementary and self-contained. The evenness proof via theta functional equation is in every analytic number theory textbook.

---

## 8. Summary Table

| Condition | Required by Pólya | Satisfied by Φ | Proof Method | Status |
|-----------|-------------------|-----------------|-------------|--------|
| (i) K > 0 | Yes | Yes | 2π > 3 (algebraic) + evenness | ✅ |
| (ii) K even | Yes | Yes | Theta functional equation | ✅ |
| (iii) K ∈ L¹ | Yes | Yes | Super-exponential decay | ✅ |
| (iv) (log K)″ ≤ 0 | Yes | Yes | IA [0,1] + perturbation (1,∞) | (audited separately) |
| (v) Decay | Yes | Yes | e^{−πe^{2u}} ≫ e^{−|u|^{2+δ}} | ✅ |
| (vi) Real analytic near 0 | Yes | Yes | Uniform convergent series of analytic functions | ✅ |

---

## 9. GAPS Identified

### GAP 1 (None): All conditions verified

No gaps were found in the verification of conditions (i), (ii), (iii), (v), (vi). Each condition is either elementary (positivity, integrability, decay) or classical (evenness via theta functional equation, analyticity via uniform convergence).

### Observation 1: Positivity for u < 0 is non-elementary

The positivity argument for u < 0 depends on the theta functional equation (Poisson summation), which is a standard but non-trivial result. This is not a gap — Poisson summation is a theorem — but it is worth noting that the "elementary" positivity proof (2π > 3) only covers u ≥ 0.

### Observation 2: The paper correctly added condition (vi)

The updated Theorem 1 (lines 72–82 of `main.tex`) now includes condition (v): "K is real analytic on a neighborhood of the origin." The Remark (lines 88–92) correctly explains why this condition is essential, using the e^{−|t|³} counterexample. This was a critical fix identified in `polya_theorem_red_alert_audit.md`.

---

## 10. Verdict

**PHI PROPERTIES VERIFIED.**

All five non-computational conditions of Pólya's theorem are rigorously satisfied by Φ:
- Positivity: elementary for u ≥ 0 (2π > 3), extended by evenness
- Evenness: classical (theta functional equation / Poisson summation)
- Integrability: trivial (super-exponential decay)
- Decay: vastly exceeds the requirement (by a factor of 10^{12,000,000} at u = 8)
- Real analyticity: uniform convergence of analytic series

No gaps were found. The remaining condition (log-concavity) is the computational core of the proof, verified by interval arithmetic and audited separately.
