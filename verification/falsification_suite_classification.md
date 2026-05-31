# Falsification Suite Classification

## Overview

The project contains 6 primary falsification scripts (`falsify_own_proof.py` through `falsify_final.py`) implementing 32 numbered attacks, plus 8 auxiliary scripts. This document classifies each attack.

### Classification Key

- **proof-critical**: Directly tests a load-bearing claim in the proof chain. Failure would invalidate the proof.
- **certificate-verification**: Verifies correctness of a computational certificate (IA enclosure, derivative formula, etc.).
- **numerical-sanity**: Tests that computed values are reasonable, but is not rigorous. Failure would be a red flag, not a disproof.
- **convention-check**: Verifies that the formula/normalization matches the standard mathematical definition.
- **bug-detection**: Tests implementation correctness (algebraic formulas, library behavior).
- **historical-contextual**: Checks background theorems, prior work, or mathematical context. Does not directly prove or disprove anything in the proof chain.

### Status Key

- **Proves**: The test, if it passes, constitutes part of a rigorous argument.
- **Increases confidence**: The test increases confidence but does not constitute proof.

---

## Attacks 1–5: `falsify_own_proof.py`

| # | Target Claim | Failure Condition | Classification | Proves or Confidence? |
|---|---|---|---|---|
| 1 | Pólya's decay condition is necessary | Cosine transform of e^{-t^3} does NOT have complex zeros | historical-contextual | Increases confidence — confirms decay condition is non-vacuous, but does not prove Pólya's theorem itself |
| 2 | Φ(u) > 0 for all u ≥ 0 | Find u where Φ(u) ≤ 0 in [0,1] with 10,001 points | numerical-sanity | Increases confidence only — point sampling cannot prove positivity |
| 3 | Φ is even: Φ(-u) = Φ(u) | |Φ(u) - Φ(-u)| / |Φ(u)| > 10^{-50} at any test point | numerical-sanity | Increases confidence only — tests at 8 points, not rigorous |
| 4 | Q_Φ(u) < 0 for all u ≥ 0 | Find any u where Q_Φ(u) ≥ 0 among 7,001 test points (dense + random + adversarial near u ≈ 0.98) | proof-critical | Increases confidence only — this is the POINT-SAMPLING counterpart of the IA certificate; it cannot prove Q < 0 but finding Q ≥ 0 would disprove it |
| 5 | Φ decays faster than e^{-u^3} | log₁₀(Φ(u)) ≥ log₁₀(e^{-u^3}) at u = 2, 3, 5, or 8 | numerical-sanity | Increases confidence — checks decay at 4 points, not rigorous |

## Attacks 6–10: `falsify_advanced.py`

| # | Target Claim | Failure Condition | Classification | Proves or Confidence? |
|---|---|---|---|---|
| 6 | Our Φ formula matches the standard xi kernel | ∫Φ(u)du ≠ ξ(1/2) or ∫Φ(u)cos(γ₁u)du ≠ 0 (ratio deviates from 1.0 by >1%) | convention-check | Increases confidence — numerical integration, not rigorous |
| 7 | Perturbation constant C is correct | Implied C from explicit computation at u=1 is unreasonably large or bound fails | certificate-verification | Increases confidence — verifies the C=204 computation at a single point |
| 8 | Φ is C² at u=0 | Φ''(0) series does not converge with increasing N | numerical-sanity | Increases confidence — convergence check, not a proof of smoothness |
| 9 | No circularity: Pólya doesn't assume RH | Identify logical circularity in the proof chain | proof-critical | Increases confidence — this is a logical/conceptual audit, not a computation. The analysis is correct: Pólya 1927 is independent of RH. |
| 10 | mpmath.iv is trustworthy | π, e, e^{-π}, or compound expression not contained in IA interval | bug-detection | Increases confidence — tests 4 containment cases, not exhaustive |

## Attacks 11–15: `falsify_structural.py`

| # | Target Claim | Failure Condition | Classification | Proves or Confidence? |
|---|---|---|---|---|
| 11 | Pólya's Satz II states what we claim | The theorem as cited doesn't match the original 1927 German text | proof-critical | **Neither — this attack is UNRESOLVED.** The script itself notes this is "the weakest link." It identifies that the exact statement needs verification against the original German text and that Csordas-Varga 1989 lists multiple theorems. The paper now cites secondary sources (Csordas-Varga, Levin) rather than the primary source. |
| 12 | Derivative formulas for φ_n', φ_n'' are correct | Symbolic derivatives disagree with finite differences by >10^{-10} | bug-detection | Increases confidence — **historically detected a real bug** (g'' coefficient 81/4 → 81/2). This is the most valuable attack in the suite. |
| 13 | Perturbation bound improves monotonically for u > 1 | |ΔQ|/|Q_{φ₁}| increases at some u > 1 | certificate-verification | Increases confidence — checks monotonicity at 5 points |
| 14 | Approach is specific to ζ (doesn't trivially give GRH) | Method works unchanged for Dirichlet L-functions | historical-contextual | Increases confidence — conceptual analysis, not computation. Correctly identifies that L-function kernels involve characters and may not be positive. |
| 15 | Log-concavity of Φ is equivalent to RH (no shortcut) | Log-concavity is strictly weaker than RH | historical-contextual | Increases confidence — correctly establishes logical equivalence (given unconditional decay), ruling out circularity |

## Attacks 16–20: `falsify_edge_cases.py`

| # | Target Claim | Failure Condition | Classification | Proves or Confidence? |
|---|---|---|---|---|
| 16 | Series formula is exactly even (via theta functional equation) | Φ(0.5) ≠ Φ(-0.5) to 40+ digits when summing 49 terms | convention-check | Increases confidence — verifies that the individual-term formula (which is NOT term-by-term even) correctly sums to an even function via the functional equation |
| 17 | mpmath computes exp correctly at 50 digits | exp(1) from 200-term Taylor series disagrees with mpmath.exp(1) | bug-detection | Increases confidence — redundant cross-check of mpmath internals |
| 18 | mpmath.iv actually computes intervals (not degenerate) | exp([0.4, 0.6]) width is not significantly wider than exp([0.5, 0.5]) width | bug-detection | Increases confidence — tests that IA library tracks interval widths |
| 19 | Q_f = f''f - f'² correctly characterizes log-concavity | Q_{e^{-t²}} ≠ -2e^{-2t²} | convention-check | Increases confidence — verifies formula on a known log-concave function |
| 20 | g' coefficient 15/2 is correct | Symbolic g' disagrees with finite differences at test points | bug-detection | Increases confidence — finite difference verification at 8 (u,n) combinations |

## Attacks 21–26: `falsify_deep.py`

| # | Target Claim | Failure Condition | Classification | Proves or Confidence? |
|---|---|---|---|---|
| 21 | E'' = (-4πn²e^{2u} + 4π²n⁴e^{4u})E is correct | Symbolic E'' disagrees with mpmath.diff at any test point | bug-detection | Increases confidence — tests 12 (u,n) combinations |
| 22 | Full product rule assembly φ₁'' = g''E + 2g'E' + gE'' | Assembled φ₁'' disagrees with mpmath.diff(φ₁, u, 2) | bug-detection | Increases confidence — tests 6 u values. This is the most important derivative cross-check. |
| 23 | Q_Φ is symmetric: Q_Φ(-u) = Q_Φ(u) | Q at positive and negative u disagree by >10^{-8} | numerical-sanity | Increases confidence — tests 4 u values using finite differences |
| 24 | Integral representation holds at t=5 | ∫Φ(u)cos(5u)du ≠ Re(ξ(1/2+5i)) (ratio deviates from 1.0 by >1%) | convention-check | Increases confidence — cross-checks the integral representation at a nonzero t value |
| 25 | Factor of 4 in Φ = 4Σφ_n preserves Q sign | Q(4·sum) / Q(sum) ≠ 16 | convention-check | Increases confidence — verifies algebraic identity Q_{cf} = c²Q_f |
| 26 | IA enclosure on [0.5, 0.501] contains all point evaluations | Any of 100 random point Q values falls outside IA enclosure | certificate-verification | Increases confidence — spot-checks IA containment property |

## Attacks 27–32: `falsify_final.py`

| # | Target Claim | Failure Condition | Classification | Proves or Confidence? |
|---|---|---|---|---|
| 27 | Pólya's theorem holds for e^{-cosh(t)} | Argument principle finds complex zeros of cosine transform of e^{-cosh(t)} | historical-contextual | Increases confidence — tests Pólya on an independent log-concave kernel with superexponential decay. Failure would undermine Pólya's theorem itself. |
| 28 | Differentiated series Σ|φ_n''| converges at u=0 | Partial sums do not converge | numerical-sanity | Increases confidence — checks that term-by-term differentiation is valid |
| 29 | E' = -2πn²e^{2u}E is correct | Symbolic E' disagrees with mpmath.diff | bug-detection | Increases confidence — tests 12 (u,n) combinations |
| 30 | 15/2 coefficient in g' is correct | Symbolic g' with 15/2 disagrees with mpmath.diff | bug-detection | Increases confidence — redundant with attack 20 but uses mpmath.diff directly |
| 31 | Q_Φ is negative everywhere (adversarial search) | Q_Φ ≥ 0 at any of 15,001 points on [0.5, 2.0] | proof-critical | Increases confidence — most adversarial point search. Finds the u where Q is closest to zero. Does NOT prove Q < 0. |
| 32 | End-to-end: Ξ vanishes at γ₂ = 21.022... | ∫Φ(u)cos(γ₂u)du is not close to zero | convention-check | Increases confidence — verifies the integral representation at the second Riemann zero |

## Auxiliary Scripts (not numbered 1–32)

| Script | Purpose | Classification | Notes |
|---|---|---|---|
| `audit_external.py` | Audit 5 external RH proof claims (Gershon, preprint-0159, AIVisions, Geiger, self) against standardized checks | historical-contextual | Framework for cross-checking other proofs; also self-audits |
| `test_logconcavity.py` | 7-test stress battery: positivity, Q<0 scan, evenness, Xi at γ₁, log-derivative profile, integrability, xi cross-check | numerical-sanity | Comprehensive but non-rigorous point-sampling suite |
| `test_exp_t4.py` | Does cosine transform of e^{-t⁴} have complex zeros? | historical-contextual | Confirms NO complex zeros for p=4 (even integer), consistent with Csordas-Varga |
| `test_exp_t4_argprinc.py` | Argument principle zero count for e^{-t⁴} in rectangles | historical-contextual | More rigorous than test_exp_t4.py; uses winding numbers |
| `gram_violations.py` | Find Gram's law violations (requires `riemann` module) | numerical-sanity | Standard RH consistency check, not directly related to the proof |
| `lehmer_pairs.py` | Search for Lehmer pairs / close zero pairs (requires `riemann` module) | numerical-sanity | Provides lower bounds on de Bruijn-Newman constant Λ |
| `li_sign_monitor.py` | Monitor Li coefficients λ_n for negativity (requires `riemann` module) | numerical-sanity | Any λ_n < 0 would disprove RH directly |
| `off_line_search.py` | Search for zeta zeros off the critical line (requires `riemann` module) | numerical-sanity | Direct RH falsification attempt |

## Summary Statistics

| Classification | Count (of 32) | Purpose |
|---|---|---|
| proof-critical | 3 (#4, #9, #31) | Tests that, if they found a violation, would break the proof |
| certificate-verification | 3 (#7, #13, #26) | Verifies correctness of computational certificates |
| numerical-sanity | 5 (#2, #3, #5, #8, #23, #28) | Non-rigorous consistency checks |
| convention-check | 6 (#6, #16, #19, #24, #25, #32) | Verifies formula conventions and normalizations |
| bug-detection | 8 (#10, #12, #17, #18, #20, #21, #22, #29, #30) | Tests implementation correctness |
| historical-contextual | 5 (#1, #11, #14, #15, #27) | Checks background theorems and context |

**Note on counting:** Some attacks span two categories; the primary classification is listed above. Attack counts sum to >32 because attacks #5 and #28 overlap sanity categories.

## Critical Gaps Identified

1. **Attack 11 is unresolved.** The exact statement of Pólya's "Satz II" has not been verified against the original 1927 German text. The proof relies on secondary restatements (Csordas-Varga 1989, Levin 1964). While these are reputable and widely cited, a reviewer WILL ask for a precise citation to the original theorem statement, including the exact conditions (iv) as stated in the primary source.

2. **No attack tests the IA certificate itself end-to-end.** Attacks 10, 18, 26 test IA library behavior on toy examples. But no attack independently re-runs the full 52,898-subinterval verification and checks that every subinterval passes. The Arb verification (`verify_logconcavity_arb.py`) does this, but it is not part of the falsification suite — it is a separate proof script.

3. **None of the 32 attacks constitutes a proof.** Every single one "increases confidence" rather than "proves." The actual proof-bearing components are in `proof/`, not `falsification/`. This is by design — the falsification suite is a stress test, not a proof — but the paper should make this distinction clearer.

4. **Point-sampling attacks (#2, #3, #4, #5, #31) are fundamentally non-rigorous.** They can falsify but cannot verify. A reviewer may question why they are given prominence in the paper.
