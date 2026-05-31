# Falsification Suite Audit

**Auditor:** Oz (automated verification agent)
**Date:** 2026-05-31
**Scripts audited:** 6 primary (`falsify_own_proof.py` through `falsify_final.py`)
**Total numbered attacks:** 32

---

## Classification Key

- **proof-critical**: Tests a load-bearing claim. Failure would invalidate or seriously damage the proof.
- **certificate-verification**: Verifies correctness of a computational certificate (IA, derivative formula, constant).
- **numerical-sanity**: Point-sampling or heuristic check. Can falsify but cannot verify.
- **convention-check**: Verifies formula normalization, integral representation, or algebraic identity.
- **bug-detection**: Tests implementation correctness of code or library. Historically caught real bugs.
- **historical**: Tests background theorems, prior work, or mathematical context.

---

## Complete Attack Classification

### Attacks 1–5: `falsify_own_proof.py`

| # | Name | Classification | Notes |
|---|------|---------------|-------|
| 1 | Pólya counterexample: e^{-t³} complex zeros | **proof-critical** | Now correctly tests condition (v) analyticity, not just (iv) decay. Confirms e^{-|t|³} fails (v) and has complex zeros. This is the MOST IMPORTANT falsification attack because it validates the theorem statement itself. |
| 2 | Can Φ go negative? (10,001 points on [0,1]) | numerical-sanity | Point-sampling cannot prove positivity. Would catch gross errors only. |
| 3 | Is Φ even? (8 test points) | numerical-sanity | Tests Φ(u) vs Φ(-u) at 8 points. Verifies functional equation numerically. |
| 4 | Search for Q_Φ ≥ 0 (7,001 points) | **proof-critical** | The point-sampling counterpart of the IA certificate. Dense + random + adversarial near u≈0.98. Cannot prove Q<0 but finding Q≥0 would disprove the central claim. |
| 5 | Decay rate check (4 points) | numerical-sanity | Checks log₁₀(Φ) < log₁₀(e^{-u³}) at u=2,3,5,8. Trivially satisfied. |

### Attacks 6–10: `falsify_advanced.py`

| # | Name | Classification | Notes |
|---|------|---------------|-------|
| 6 | Convention: ∫Φ du = ξ(1/2)? | convention-check | Verifies our Φ formula integrates to ξ(1/2)≈0.4971 to 15 digits, and vanishes at γ₁. |
| 7 | Explicit C=204 computation | certificate-verification | Computes all tail ratios ε, ε', ε'' at u=1 and derives C=204. Verified. |
| 8 | Is Φ C² at u=0? | numerical-sanity | Series convergence of Φ''(0) with N=1..50. Converges rapidly. |
| 9 | Tautology / circularity check | **proof-critical** | Logical audit: does Pólya assume RH? No — it's a general kernel theorem. Does our IA assume RH? No. No circularity found. |
| 10 | mpmath.iv containment (π, e, e^{-π}, compound) | bug-detection | Tests 4 IA containment cases at 50-digit precision. All pass. |

### Attacks 11–15: `falsify_structural.py`

| # | Name | Classification | Notes |
|---|------|---------------|-------|
| 11 | Does Pólya's Satz II say what we claim? | **proof-critical** | The script itself flags this as the weakest link. Identifies that the exact conditions need verification against the original 1927 German text. The paper now cites three secondary sources. STATUS: PARTIALLY RESOLVED — paper now includes (v) analyticity, but primary source still unverified. |
| 12 | Derivative formulas vs finite differences | bug-detection | **Historically detected a real bug:** g'' coefficient was 81/4 instead of 81/2. This is the single most valuable attack in the suite. Tests at 18 (u,n) combinations at 60-digit precision with h=10^{-15}. |
| 13 | Perturbation bound monotonicity for u>1 | certificate-verification | Tests |ΔQ|/|Q_{φ₁}| at u=1.0, 1.2, 1.5, 2.0, 3.0. All decrease. |
| 14 | Approach specific to ζ (doesn't trivially give GRH)? | historical | Correctly identifies that L-function kernels involve characters, may not be positive. Reassuring. |
| 15 | Is log-concavity of Φ equivalent to RH? | historical | Correctly establishes logical equivalence (given unconditional decay). No circularity. |

### Attacks 16–20: `falsify_edge_cases.py`

| # | Name | Classification | Notes |
|---|------|---------------|-------|
| 16 | Series formula exactly even via theta functional equation? | convention-check | Individual φ_n(u) ≠ φ_n(-u), but sum agrees to 40+ digits via functional equation cancellation. |
| 17 | mpmath.exp correct at 50 digits? | bug-detection | Cross-checks exp(1) against 200-term Taylor series. Agreement to 50+ digits. |
| 18 | Does mpmath.iv actually track intervals? | bug-detection | Tests width propagation: exp([0.4,0.6]) is wider than exp([0.5,0.5]). Confirms IA is functional. |
| 19 | Is Q_f = f''f − f'² the right formula? | convention-check | Verifies on Gaussian e^{-t²}: Q = -2f² exactly. Formula confirmed. |
| 20 | g' coefficient 15/2 correct? | bug-detection | Symbolic vs finite differences at 8 (u,n) combinations. Agrees. |

### Attacks 21–26: `falsify_deep.py`

| # | Name | Classification | Notes |
|---|------|---------------|-------|
| 21 | E'' formula correct? | bug-detection | Symbolic vs mpmath.diff at 12 (u,n) combinations. Max error < 10^{-15}. |
| 22 | Full product rule assembly φ₁'' = g''E + 2g'E' + gE''? | bug-detection | Assembled φ₁'' vs mpmath.diff(φ₁, u, 2) at 6 u values. Max error < 10^{-15}. Most important derivative cross-check. |
| 23 | Q_Φ symmetric at positive/negative u? | numerical-sanity | Tests Q(+u) vs Q(-u) at 4 values via finite differences. Uses numerical differentiation (h=10^{-8}), limited by FD accuracy. |
| 24 | ∫Φ cos(5u) du = Re(ξ(1/2+5i))? | convention-check | Cross-checks integral representation at t=5. Ratio ≈ 1.0. **NOTE:** This is the Ξ(5) convention check referenced in the task. |
| 25 | Factor of 4 preserves Q sign? | convention-check | Q(4·sum)/Q(sum) = 16. Algebraic identity Q_{cf} = c²Q_f verified. |
| 26 | IA enclosure contains all point evaluations? | certificate-verification | 100 random points in [0.5, 0.501] all contained in IA enclosure. Spot-check only. |

### Attacks 27–32: `falsify_final.py`

| # | Name | Classification | Notes |
|---|------|---------------|-------|
| 27 | Pólya on e^{-cosh(t)} | **proof-critical** | Tests Pólya's theorem on an independent kernel satisfying ALL conditions (positive, even, L¹, log-concave, superexp decay, real analytic). Finds only real zeros via winding number. Confirms Pólya is correct on a known example. |
| 28 | Σ|φ_n''| converges at u=0? | numerical-sanity | Partial sums of |φ_n''(0)| for n=1..29 converge rapidly. Validates term-by-term differentiation. |
| 29 | E' formula correct? | bug-detection | Redundant with attack 21 approach but for first derivative. 12 (u,n) combinations. |
| 30 | 15/2 coefficient in g' via mpmath.diff? | bug-detection | Redundant with attack 20 but uses mpmath.diff directly instead of finite differences. |
| 31 | Adversarial Q search on [0.5, 2.0] (15,001 points) | **proof-critical** | Finds the u where Q is closest to zero. Still negative. The densest point-sampling attack. |
| 32 | End-to-end: Ξ vanishes at γ₂ = 21.022? | convention-check | ∫Φ(u)cos(γ₂u)du ≈ 0 to 10^{-10}. Full pipeline check at second Riemann zero. |

---

## Summary Statistics

| Classification | Count | Attack Numbers |
|---------------|-------|----------------|
| proof-critical | 6 | 1, 4, 9, 11, 27, 31 |
| certificate-verification | 3 | 7, 13, 26 |
| numerical-sanity | 5 | 2, 3, 5, 8, 23, 28 |
| convention-check | 7 | 6, 16, 19, 24, 25, 32 |
| bug-detection | 9 | 10, 12, 17, 18, 20, 21, 22, 29, 30 |
| historical | 3 | 14, 15 |

(Attacks 5/28 and 23 span categories; primary classification shown.)

---

## Assessment of Proof-Critical Attacks

### Attack 1 (Pólya counterexample): WELL-DESIGNED
Now correctly tests condition (v) analyticity. The e^{-|t|³} example satisfies (i)–(iv) but fails (v) and has complex zeros. This validates that the theorem conditions are not vacuous. **However:** the attack uses the one-sided transform ∫₀^∞ e^{-t³}cos(zt)dt, and the connection to the even extension's zeros is stated but not rigorously verified in the script.

### Attack 4 (Q search, 7001 points): USEFUL BUT LIMITED
Dense + random + adversarial sampling is a reasonable falsification strategy. The adversarial focus near u≈0.98 is well-chosen (where IA had the tightest bounds). But 7,001 points cannot prove Q<0 — only the IA certificate does that.

### Attack 9 (Circularity): CORRECT
The analysis is sound: Pólya 1927 makes no reference to zeta or RH. The IA computation uses only the series definition of Φ. No circularity.

### Attack 11 (Pólya citation): PARTIALLY RESOLVED
The paper now includes condition (v) and correctly states the analyticity requirement. The e^{-|t|³} remark has been fixed. However, the original German text of Satz II still has not been independently verified. This remains a known gap.

### Attack 27 (Pólya on e^{-cosh t}): WELL-DESIGNED
e^{-cosh(t)} is an ideal test case: positive, even, L¹, log-concave ((log K)'' = -cosh(t) < 0), superexponentially decaying, and real analytic. The winding number calculation confirms only real zeros in [0,15]×[-2,2]. This directly tests Pólya's theorem on an independent kernel.

### Attack 31 (Adversarial Q search): USEFUL
The 15,001-point search on [0.5, 2.0] finds the closest approach of Q to zero. This is the most adversarial point-sampling attack, but like all point-sampling, it cannot prove Q<0.

---

## What the Suite Does Well

1. **Bug detection works.** Attack 12 historically found a real coefficient error (81/4 → 81/2). This alone justifies the entire suite.
2. **Convention checks are thorough.** Attacks 6, 16, 24, 32 cross-check the integral representation at ξ(1/2), γ₁, t=5, and γ₂. This rules out normalization or sign convention errors.
3. **Derivative verification is comprehensive.** Attacks 12, 20, 21, 22, 29, 30 verify every component of the product-rule assembly against independent computation. This is the strongest part of the suite.
4. **Pólya theorem tests (1, 27) are creative.** Testing the theorem on known kernels (one satisfying, one failing conditions) is a sound approach to validating the theorem statement.

## What the Suite Does NOT Do

1. **None of the 32 attacks constitutes proof.** Every attack "increases confidence" — none proves anything. The proof-bearing components are the IA certificate and the algebraic core, which live in `proof/`, not `falsification/`.

2. **No attack independently re-runs the full IA.** The Arb/FLINT independent verification exists in `proof/verify_logconcavity_arb.py` but is NOT part of this falsification suite. This is the most important gap in the suite's coverage.

3. **Point-sampling attacks are fundamentally asymmetric.** They can find counterexamples (Q≥0) but cannot prove absence. The paper should not imply these contribute to proof status.

4. **Bug-detection attacks test the same derivative formulas both libraries use.** If a formula error exists in the mathematical derivation (not the code), both mpmath and Arb would propagate it. The cross-check against mpmath.diff partially addresses this, but mpmath.diff uses numerical differentiation which has its own error characteristics.

---

## Verdict

**FALSIFICATION SUITE: WELL CLASSIFIED, RHETORICALLY APPROPRIATE (with caveats)**

The suite is genuinely useful engineering that caught a real bug and provides strong confidence in implementation correctness. The classification into proof-critical vs. evidence is sound. The suite should be presented as what it is: a stress test that increases confidence, NOT proof infrastructure.

**Recommended paper language:** "We subjected every link in the proof chain to 32 systematic falsification attacks. Attack 12 historically detected and corrected a coefficient error. All attacks failed to falsify the proof. These attacks increase confidence but do not constitute proof; the rigorous components are the IA certificate (Theorem 5) and algebraic core (Theorem 4)."

**Warning against overweighting:** The paper's abstract gives significant space to the falsification suite, which may mislead readers into thinking it contributes to proof rigor. In a journal submission, this should be relegated to an appendix with a brief mention in the main text.
