# Φ Positivity Proof

## 1. Claim

Φ(u) > 0 for all u ∈ ℝ.

This is hypothesis (i) of Pólya's theorem as applied in the paper.

---

## 2. Structure

Since Φ is even (Φ(−u) = Φ(u)), it suffices to prove Φ(u) > 0 for u ≥ 0.

Φ(u) = 4 Σ_{n=1}^∞ φₙ(u)

where φₙ(u) = (2π²n⁴e^{9u/2} − 3πn²e^{5u/2}) e^{−πn²e^{2u}}.

It suffices to show that each φₙ(u) > 0 for u ≥ 0 and n ≥ 1.

---

## 3. Term-by-Term Positivity (Self-Contained Proof)

### Step 1: Factor φₙ

φₙ(u) = πn²e^{5u/2} (2πn²e^{2u} − 3) e^{−πn²e^{2u}}

Let hₙ(u) = 2πn²e^{2u} − 3.

Then: φₙ(u) = πn²e^{5u/2} · hₙ(u) · e^{−πn²e^{2u}}

The factors πn²e^{5u/2} > 0 and e^{−πn²e^{2u}} > 0 are always positive. So:

**φₙ(u) > 0 ⟺ hₙ(u) > 0 ⟺ 2πn²e^{2u} > 3.**

### Step 2: Verify hₙ(u) > 0 for n ≥ 1, u ≥ 0

For n ≥ 1 and u ≥ 0:

2πn²e^{2u} ≥ 2π · 1² · e⁰ = 2π ≈ 6.2832 > 3 ✓

**Therefore hₙ(u) > 0 for all n ≥ 1, u ≥ 0.** □

### Step 3: Conclude

Since every term φₙ(u) > 0 for n ≥ 1, u ≥ 0:

Φ(u) = 4 Σ_{n=1}^∞ φₙ(u) > 0 for u ≥ 0. □

---

## 4. Citation Chain

| Source | Statement | Proof method |
|--------|-----------|-------------|
| Paper, Proposition 1(i) | Φ(u) > 0 for all u ≥ 0 | "Classical; see Titchmarsh §2.10 and Csordas–Varga Theorem A" |
| Csordas–Varga 1990, Theorem A(i) | For each n ≥ 1, Φₙ(t) > 0 for all t ≥ 0 | Uses 2πn²e^{4t} − 3 > 0 (their variable convention uses e^{4t}) |
| Titchmarsh 1986, §2.10 | Φ(u) > 0 | Derives from Jacobi theta properties |
| Chung 1976 | H(y) > 0 for y > 0 | Uses functional equation: H(y) > 0 for y ≥ 1 is obvious, then yH(y) = H(1/y) extends to y < 1 |
| Newman 1976 | H(y) > 0 for y > 0 | Same argument |
| Paper, §4 (algebraic core) | h(u) = 2πe^{2u} − 3 > 0 for u ≥ 0 | Direct: 2π > 3 |

**Strongest available proof:** The term-by-term argument in §3 above. It is elementary and self-contained: it uses only 2π > 3.

---

## 5. Extending to u < 0: Evenness

Φ(−u) = Φ(u) follows from the theta functional equation. The argument:

### From the theta function

The Jacobi theta function θ(x) = Σ_{n=−∞}^∞ e^{−πn²x} satisfies:

θ(1/x) = √x · θ(x)   (x > 0)

This is the modular identity, proved via Poisson summation.

### Consequence for H(y)

H(y) = d/dy [y² d/dy G(y)] where G(y) = θ(y²) = Σ e^{−πn²y²}.

The functional equation θ(1/x) = √x · θ(x) implies (via direct computation, see Lagarias–Montague 2011, Lemma 3.1):

yH(y) = H(1/y)   (y > 0)

### Consequence for Φ

With Φ(u) = 2e^u H(e^u) (in the Lagarias–Montague normalization, up to constants):

Φ(−u) = 2e^{−u} H(e^{−u})

Using yH(y) = H(1/y) with y = e^{−u}: e^{−u} H(e^{−u}) = H(e^u)

So Φ(−u) = 2H(e^u) = 2e^u · e^{−u} H(e^u) = ... 

Actually, let me be more precise. The paper's Φ(u) at the level of the series is:

Φ(u) = 4 Σ_{n=1}^∞ (2π²n⁴e^{9u/2} − 3πn²e^{5u/2}) e^{−πn²e^{2u}}

This is NOT obviously even from the series representation (each term is NOT even in u). The evenness comes from the theta functional equation, which mixes different terms of the series.

**Key point:** The evenness of Φ is a DEEP property following from the modular identity of the Jacobi theta function. It is NOT visible term-by-term.

**The paper correctly identifies this** (Proposition 1(ii)): "Properties (i)–(iii) are classical; see Titchmarsh §2.10 and Csordas–Varga Theorem A."

---

## 6. Numerical Verification

The paper performs two numerical checks:

1. **Positivity check:** Φ(u) > 0 at 10,001 uniformly spaced points on [0, 1], with min = 5.51 × 10⁻⁷ at u = 1.

2. **Evenness check:** |Φ(u) − Φ(−u)|/|Φ(u)| < 10⁻⁷⁰ at 8 test points.

These are consistency checks, not proofs. But they provide strong numerical evidence.

---

## 7. Where Positivity is Used

Positivity of Φ enters the proof at multiple points:

1. **Pólya's theorem:** Requires K(t) > 0 (hypothesis (i)).

2. **Log-concavity definition:** (log Φ)″ requires Φ > 0 for log Φ to be defined.

3. **Q_Φ formulation:** Q_Φ = Φ″Φ − (Φ′)² < 0 is equivalent to (log Φ)″ < 0 only when Φ > 0.

4. **Perturbation bound:** The ratio R/φ₁ requires φ₁ > 0.

---

## 8. Potential Gaps

### 8a. Positivity for u < 0

The term-by-term argument only works for u ≥ 0 (since hₙ(u) = 2πn²e^{2u} − 3 can be negative for sufficiently negative u). For u < 0, positivity relies on evenness, which in turn relies on the theta functional equation.

**Is the theta functional equation rigorously established?** Yes — it follows from Poisson summation, which is a theorem (not a conjecture). The derivation is in every analytic number theory textbook (Titchmarsh, Edwards, Iwaniec–Kowalski).

**Status:** ✅ No gap.

### 8b. Does positivity hold at the series level?

The paper defines Φ as a series. For u ≥ 0, each term is positive and the series converges absolutely (by the exponential decay factors), so the sum is positive.

For u < 0, individual terms may be negative (when hₙ(u) < 0 for small n), but the full sum Φ(u) = Φ(−u) > 0 by evenness.

**Status:** ✅ Correct but relies on evenness for u < 0.

### 8c. Positivity at u = 0

At u = 0: h₁(0) = 2π − 3 ≈ 3.28 > 0.
φ₁(0) = π(2π − 3)e^{−π} ≈ 3.28π e^{−π} ≈ 0.444.
Φ(0) ≈ 4(0.444 + small corrections) ≈ 1.78.

Exact value: Φ(0) = 2ξ(1/2)/... Actually, from ∫₀^∞ Φ du = ξ(1/2), Φ(0) is not directly ξ(1/2). But numerical evaluation gives Φ(0) ≈ 1.7867, which is clearly positive.

**Status:** ✅

---

## 9. Summary

| Component | Status | Method |
|-----------|--------|--------|
| φₙ(u) > 0 for n ≥ 1, u ≥ 0 | ✅ Proven | Elementary: 2π > 3 |
| Φ(u) > 0 for u ≥ 0 | ✅ Proven | Sum of positive terms |
| Φ(u) = Φ(−u) (evenness) | ✅ Classical | Theta functional equation |
| Φ(u) > 0 for u < 0 | ✅ By evenness | Φ(−u) = Φ(u) > 0 |
| Numerical verification | ✅ | 10,001 points, min ≈ 5.5 × 10⁻⁷ |

**VERDICT:** The positivity of Φ is rigorously established for u ≥ 0 by the elementary argument 2π > 3 applied term-by-term, and extended to all u by the classical evenness property. This is the strongest possible proof — no numerical computation is needed.

The critical fact 2π > 3 is what makes the proof work. If 2π were less than 3 (which it is not, since π ≈ 3.14159), the n = 1 term would be negative near u = 0 and the proof would fail. The margin is 2π − 3 ≈ 3.28, which is substantial.
