# Tail Bound Uniform Proof: λ(u) ≤ λ(1) < 1 for All u ≥ 1

**Claim under audit:** The perturbation ratio λ(u) = |ΔQ(u)| / |Q_{φ₁}(u)| satisfies
λ(u) ≤ λ(1) = 1.95 × 10⁻²⁷ < 1 for all u ≥ 1, ensuring Q_Φ < 0 on [1, ∞).

**Methodology:** Analytic proof with numerical verification via `compute_lambda_tail.py`.

---

## 1. Setup and Definitions

Write Φ = 4(φ₁ + R) where R = Σ_{n≥2} φ_n. Then Q_Φ = 16·Q_{φ₁+R} = 16(Q_{φ₁} + ΔQ).
Since Q_{φ₁} < 0 (Algebraic Core, Theorem 3 of the paper), the sign of Q_Φ is determined by
whether |ΔQ| < |Q_{φ₁}|, equivalently whether λ(u) := |ΔQ(u)|/|Q_{φ₁}(u)| < 1.

We decompose λ(u) = C(u) · ε(u) where:
- ε(u) := |R(u)| / φ₁(u) (the tail ratio)
- C(u) := λ(u) / ε(u) = |ΔQ(u)| / (ε(u) · |Q_{φ₁}(u)|) (the amplification constant)

## 2. Monotonic Decrease of ε(u) for u ≥ 0

### Lemma 2.1 (Term-by-term ratio bound)
For each n ≥ 2, define r_n(u) := φ_n(u) / φ₁(u). Then r_n(u) is strictly decreasing for u ≥ 0.

**Proof:**
Write φ_n = g_n · E_n where g_n(u) = πn²e^{5u/2}(2πn²e^{2u} - 3) and E_n = e^{-πn²e^{2u}}.

Then r_n(u) = (g_n/g_1) · e^{-π(n²-1)e^{2u}}.

Compute d/du[log r_n]:

d/du[log r_n] = d/du[log(g_n/g_1)] - 2π(n²-1)e^{2u}

For the prefactor ratio:
- log(g_n/g_1) = log(n²) + log(2πn²e^{2u} - 3) - log(2πe^{2u} - 3)
- d/du[log(g_n/g_1)] = 4πn²e^{2u}/(2πn²e^{2u} - 3) - 4πe^{2u}/(2πe^{2u} - 3)

Denote h_n(u) = 2πn²e^{2u} - 3 and h_1(u) = 2πe^{2u} - 3. Then:
- d/du[log(g_n/g_1)] = 4πe^{2u}[n²/h_n - 1/h_1]

For n ≥ 2, u ≥ 0: h_n ≥ h_1 · n² - 3(n² - 1) (since 2πn²e^{2u} - 3 = n²(2πe^{2u} - 3) + 3(n² - 1)).

Wait — actually h_n = n²·h_1 + 3(n² - 1). So n²/h_n = n²/(n²h_1 + 3(n² - 1)) < 1/h_1.

Therefore d/du[log(g_n/g_1)] = 4πe^{2u}[n²/h_n - 1/h_1] < 0.

Combined: d/du[log r_n] = (negative) - 2π(n²-1)e^{2u} < 0 for all u ≥ 0.

Each ratio r_n(u) is strictly decreasing. ∎

### Corollary 2.2
ε(u) = |R(u)|/φ₁(u) = Σ_{n≥2} r_n(u) is strictly decreasing for u ≥ 0, being a sum of
strictly decreasing positive functions.

### Quantitative decay rate
The dominant term (n=2) gives:

d/du[log ε] ≈ d/du[log r_2] ≈ (small correction) - 2π·3·e^{2u} = -6πe^{2u}

Numerical values:
- u=1.0: d/du[log ε] ≈ -6π·e² ≈ -139.3
- u=1.5: d/du[log ε] ≈ -6π·e³ ≈ -378.6
- u=2.0: d/du[log ε] ≈ -6π·e⁴ ≈ -1029.2

The decay is doubly-exponential in u.

## 3. Growth Rate of C(u)

The constant C(u) = |ΔQ|/(ε · |Q_{φ₁}|) is a ratio of smooth functions. Expanding ΔQ:

ΔQ = φ₁''R + R''φ₁ + R''R - 2φ₁'R' - R'²

Dividing by ε · |Q_{φ₁}|:
- The dominant terms φ₁''R/(ε Q_{φ₁}) = φ₁''φ₁/(φ₁''φ₁ - φ₁'²) → bounded
- Similarly R''φ₁/(ε Q_{φ₁}) involves (R''/R)·(R/φ₁)·φ₁²/Q_{φ₁} → bounded ratios times ε'' / ε

The key point: C(u) is a ratio of polynomial-exponential terms in e^{2u}.

### Numerical measurement of C(u) growth rate:

| u   | C(u)     | log₁₀(C) | Δ log₁₀(C)/Δu |
|-----|----------|-----------|----------------|
| 1.0 | 203.6    | 2.31      | —              |
| 1.1 | 249.9    | 2.40      | 0.88           |
| 1.2 | 306.5    | 2.49      | 0.88           |
| 1.3 | 375.5    | 2.57      | 0.88           |
| 1.5 | 562.8    | 2.75      | 0.88           |
| 2.0 | 1538.7   | 3.19      | 0.87           |
| 2.5 | 4191.3   | 3.62      | 0.87           |
| 3.0 | 11401.7  | 4.06      | 0.87           |
| 5.0 | 622778.6 | 5.79      | 0.87           |

C(u) grows approximately as e^{2u} (i.e., d/du[log C] ≈ 2.0).
More precisely: d/du[log₁₀ C] ≈ 0.87, so d/du[log C] ≈ 0.87 · ln(10) ≈ 2.0.

## 4. Monotonicity of λ(u) = C(u) · ε(u)

### Theorem 4.1
For u ≥ 1, d/du[log λ] < 0, so λ(u) is strictly decreasing.

**Proof:**

d/du[log λ] = d/du[log C] + d/du[log ε]

From section 3: d/du[log C] ≈ 2 (measured, upper bounded by some constant k < 6π)

From section 2: d/du[log ε] ≤ -6πe^{2u} (from the dominant n=2 decay term)

Therefore: d/du[log λ] ≤ k - 6πe^{2u}

At u = 1: d/du[log λ] ≤ k - 6π·e² ≈ k - 139.3

For any k < 139.3 (and in practice k ≈ 2), this is negative.
Since 6πe^{2u} is increasing in u, the inequality only gets stronger for u > 1. ∎

### Rigorous upper bound on d/du[log C]
To make this fully rigorous, we need to bound d/du[log C] independently of the numerical data.

C(u) = |ΔQ(u)| / (ε(u) · |Q_{φ₁}(u)|)

Using the expressions for ΔQ and Q_{φ₁}, and letting L = (log φ₁)' and L' = (log φ₁)'':

|Q_{φ₁}| = φ₁² · |L'|
|ΔQ| ≤ |φ₁''R| + |R''φ₁| + |R''R| + 2|φ₁'R'| + |R'²|

After dividing by ε·φ₁²|L'|, C is bounded by terms like:
- |φ₁''/φ₁| / |L'| = |L' + L²|/|L'| ≤ 1 + L²/|L'|
- (ε''/ε) · 1/|L'|

Since |L'| grows as 4πe^{2u} (from (log φ₁)'' = (log h)'' - 4πe^{2u}, and the second term dominates), and L² grows as (2πe^{2u})² (from (log φ₁)' ≈ -2πe^{2u}):

C(u) is dominated by L²/|L'| ≈ (2πe^{2u})² / (4πe^{2u}) = πe^{2u}.

So C(u) = O(e^{2u}) with d/du[log C] → 2 as u → ∞.

For the formal bound: d/du[log C] ≤ k for some finite k. In the worst case, even if k is as large as 10, we still have d/du[log λ] ≤ 10 - 6π·e^{2u} < 0 for all u > log(10/(6π))/2 ≈ -0.32. This covers all u ≥ 1 with massive margin.

## 5. Numerical Verification

Computed via `compute_lambda_tail.py` at 300-digit precision with 30 terms of R:

| u   | ε(u)       | λ(u)       | C(u)   |
|-----|------------|------------|--------|
| 1.0 | 9.59e-30   | 1.95e-27   | 203.6  |
| 1.1 | 1.91e-36   | 4.78e-34   | 249.9  |
| 1.2 | 1.26e-44   | 3.85e-42   | 306.5  |
| 1.3 | 1.28e-54   | 4.81e-52   | 375.5  |
| 1.5 | 9.98e-82   | 5.62e-79   | 562.8  |
| 2.0 | 5.37e-223  | 8.26e-220  | 1538.7 |
| 2.5 | underflow  | underflow  | 4191.3 |
| 3.0 | underflow  | underflow  | 11401  |

Monotonicity check: λ(u) strictly decreasing at ALL test points. ✓

Paper's claimed values match:
- λ(1.0) = 1.95 × 10⁻²⁷ ✓
- λ(1.5) = 5.62 × 10⁻⁷⁹ ✓
- λ(2.0) = 8.26 × 10⁻²²⁰ ✓

## 6. Gaps and Issues Found

### GAP 1: C(u) is NOT constant (MEDIUM severity)
The paper writes "C := |ΔQ|/(ε·|Q_{φ₁}|) = 204" (Section 6, Theorem 5) and then states
"C·ε < 2×10⁻²⁷ ≪ 1" as if C is universal. In reality, C(u) grows from 204 at u=1 to
~623,000 at u=5. The paper's argument for u > 1 ("the product C(u)·ε(u) → 0") is correct
in spirit but omits the explicit demonstration that C's growth rate is bounded below ε's
decay rate.

**Impact:** The proof is not wrong — C·ε does decrease — but the paper would be strengthened
by stating explicitly that C(u) = O(e^{2u}) and therefore λ(u) ≤ O(e^{2u}) · e^{-3πe^{2u}} → 0.

### GAP 2: Missing formal derivative bound (LOW severity)
The argument d/du[log λ] = d/du[log C] + d/du[log ε] < 0 is presented here with numerical
evidence for the growth rate of C(u). A fully formal proof would require bounding d/du[log C]
analytically. The bound is straightforward (C(u) = O(e^{2u}) implies d/du[log C] ≤ 2 + o(1),
while d/du[log ε] = -6πe^{2u} + o(1)), but it is not in the paper.

### GAP 3: Prefactor ratio bound (LOW severity)
The paper's Proposition 5 states |φ_n|/φ₁ ≤ n⁴·e^{-π(n²-1)e^{2u}}, but the actual
prefactor ratio g_n/g_1 = n²(2πn²e^{2u} - 3)/(2πe^{2u} - 3) slightly exceeds n⁴
(by a factor 1 + 3(n²-1)/(n²(2πe^{2u} - 3))). This factor → 1 for large u and is at
most ~1.7 at u=0 for n=2. It does not affect any conclusion but the stated bound is not
tight.

## 7. Verdict

**TAIL PROOF PLAUSIBLE BUT INCOMPLETE**

The numerical evidence is overwhelming: λ(u) decreases monotonically and is below 10⁻²⁷
at u=1, dropping to effective zero by u=2. The analytic structure of the argument is correct.

However, the paper's Section 6 (Theorem 5) does not formally prove:
1. That C(u) is O(e^{2u}) (it states C is "bounded by some polynomial P(e^{2u})" without proof)
2. That d/du[log λ] < 0 for all u ≥ 1

The missing steps are elementary but should be included for a rigorous proof. A reviewer could
reasonably request:
- Explicit bound: C(u) ≤ π·e^{2u} + lower order terms (derivable from the structure of ΔQ/Q_{φ₁})
- Formal conclusion: d/du[log λ] ≤ 2 - 6πe^{2u} < 0 for u ≥ 0

These additions would close all gaps and make the tail argument fully rigorous.
