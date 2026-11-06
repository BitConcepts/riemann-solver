# Final Revision Report v7
# Pierson_2026_LogConcavity_RH — Audit Pass (Version 6 → Version 7)
# Prepared: 2026-06-01

---

## Overview

This report documents all fixes identified in the final audit pass of
`Pierson_2026_LogConcavity_RH(6).pdf`. Twelve issue areas were identified and
resolved as documentation deliverables. The corresponding LaTeX edits to
`paper/main.tex` are specified in each deliverable.

---

## 1. Lemma 12 Status

**Issue:** Lemma `lem:wtail` Step 1 asserted `d/du log λ ≤ 2 − 6πe^{2u}` by
deferring to `docs/uniform_wtail_bound.md`. This is unacceptable for a proof-critical
inequality.

**Fix (Route A):** `docs/lemma_12_hardening.md` provides Sublemma 12.1 with a
self-contained proof in three parts:
- Part (a): `d/du log ε*(u) ≤ −12πe^{2u} ≤ −6πe^{2u}` (fully rigorous, using
  n²−1 ≥ 3 for n ≥ 2 and dominated convergence).
- Part (b): `C_λ(u) = |ΔQ|/(ε*·|Q_{φ₁}|)` is non-increasing — proved by showing
  the exponential factors in numerator and denominator cancel identically, leaving
  a polynomial ratio that decays as O(e^{−2u}).
- Part (c): Combined bound `d/du log λ ≤ −6πe^{2u} ≤ 2 − 6πe^{2u}`.

**Result:** The bound is actually stronger than claimed (−6πe^{2u} not just
2 − 6πe^{2u}). Sublemma 12.1 must be inserted before Lemma `lem:wtail` in the paper.

**Route B fallback** (direct IA, removing the global 1.82×10^{−25} claim) is also
documented if a reviewer finds Part (b) insufficiently explicit.

**Status:** RESOLVED — paper edit required.

---

## 2. ε* Notation Cleanup Status

**Issue:** Theorem `thm:extended` defined C using old ε (C = 204 with ε_old) but
applied it to ε* (which is 2·ε_old). The notation mismatch was unexplained.

**Fix:** `docs/epsilon_star_C_consistency.md` provides:
- Explicit definitions: ε_old(u) = Σ n⁴ e^{−π(n²−1)e^{2u}}, ε*(u) = 2·ε_old(u)
- C_old = 204 (computed with ε_old), C* = 102 (correct ratio for ε*)
- Required sentence: "Using C = 204 with ε* is conservative by a factor of 2"

**Status:** RESOLVED — paper edit required.

---

## 3. C=204 Consistency Status

**Issue:** Same as §2 above. C_old = 204 was defined with ε_old. When used with ε*,
the bound 204·ε* = 2·(102·ε*) overshoots by factor 2, making it conservative.

**Fix:** The conservative argument is rigorous. After the dual definition of ε_old
and ε* is added to the paper (§2 fix), the C=204 usage is mathematically sound
(if perhaps wasteful by a factor of 2).

**Status:** RESOLVED — same paper edit as §2.

---

## 4. Theorem 13 Margin Status

**Issue:** The proof stated "minimum margin 91.3" but the final inequality used
"(log Φ)'' ≤ −93.1 + 1.82×10^{−25} < 0", creating an apparent inconsistency.

**Explanation:** 91.3 is the IA-certified margin (including interval overestimation);
93.15 ≈ 93.1 is the analytic value of |W₁(1)| (algebraically computed). These are
different quantities used without distinction.

**Fix (Option A):** `docs/theorem_13_margin_consistency.md` specifies replacing
−93.1 with −91.3 (use the IA-certified value consistently throughout the proof).

**Status:** RESOLVED — one-character substitution in paper/main.tex.

---

## 5. Theorem 14 Monotonicity Status

**Issue:** The proof said "ε is strictly decreasing" (old notation) and showed
`d/du[n⁴ e^{−π(n²−1)e^{2u}}] < 0` (derivative of ε_old term, not ε* term).

**Fix:** `docs/theorem_14_epsilon_star_monotonicity.md` specifies:
- Replace "ε is strictly decreasing" → "ε* is strictly decreasing, since it is
  twice a sum of strictly decreasing positive terms."
- Show `d/du[2n⁴ e^{−π(n²−1)e^{2u}}] = −4π(n²−1)e^{2u}·n⁴e^{...} < 0`
  (factor of 2 from ε* definition included)

Alternatively, reference Sublemma 12.1 Part (a) to avoid repetition.

**Status:** RESOLVED — notation fix only; no new mathematics.

---

## 6. Proposition 8 Ratio Status

**Issue:** The bound B_n(u)/n⁴ < 2 was asserted with a reference to an external
docs file rather than derived in the paper.

**Fix:** `docs/proposition_8_expanded_ratio.md` provides the complete 3-step algebraic
derivation:
- B_n(u) = (2πn⁴e^{2u} − 3n²)/(2πe^{2u} − 3) = n⁴ + 3(n⁴−n²)/(2πe^{2u}−3)
- B_n(u)/n⁴ = 1 + 3(1−1/n²)/(2πe^{2u}−3) ≤ 1 + 3/(2π−3) < 2

This is elementary algebra. The paper must contain it in-text.

**Status:** RESOLVED — paper edit required (inline derivation).

---

## 7. Formatting Fixes Completed

### 7a. Section §7.1 Tail Notation
`docs/section_7_1_tail_notation.md`: Subsection text provided defining R, Φ, W, W₁,
W_tail, (log(4f))'' = (log f)'', ε_old, ε*, C_old. Insert before Lemma `lem:wtail`.

### 7b. Abstract URL
`docs/abstract_url_cleanup.md`: Recommend removing URL from abstract; replace with
"public repository listed in Section~\ref{sec:reproduce}". The URL remains in §11.

### 7c. Remark 2 Analyticity Phrase
`docs/remark_2_analyticity_phrase_fix.md`: Replace "being a uniformly convergent
series of analytic functions" with "by the local Weierstrass argument in
Proposition~\ref{prop:phi_properties}~(v)".

### 7d. Appendix C Table
`docs/appendix_c_table_final_formatting.md`: Fix `\ leq` LaTeX typo → `\le` (fixes
"leq0" extraction artifact). Full corrected table provided.

### 7e. Appendix B Table
`docs/appendix_b_table_final_formatting.md`: Replace `tabular` with `tabularx`,
add `\usepackage{tabularx}` to preamble, split C3 into C3a/C3b/C3c. Full corrected
tables for both the main certificate table and SHA256 hash table provided.

---

## 8. Appendix D Corrected Count

**Was:** "Overall verdict: 15 of 18 criteria met."
**Now:** "Overall verdict: 14 of 18 criteria fully met; 3 not met; 1 partial."

Breakdown:
- 14 fully met: C-1,2,3,7,8,9,10,11,12,13,14,15,17,18
- 3 not met: C-4 (Lean IA), C-5 (Lean Pólya), C-6 (peer review)
- 1 partial: C-16 (Pólya source audit — English restatements only)

See `docs/appendix_d_count_correction.md` and `docs/appendix_d_verdict_language.md`.

---

## 9. Remaining External Dependencies

The following are documented in §sec:limitations of the paper and are not resolved
by this revision pass:

**Dependency A: Pólya 1927 Satz II (German original, paywalled)**
Status: CITED — five independent English restatements agree.
Residual risk: LOW. Requires institutional access for direct verification.
Required before top-journal submission.

**Dependency B: Computational certificates not in Lean**
Status: AXIOMATIZED — Lean axioms ia_verification_0_to_1, ia_verification_1_to_3.
Path to resolution: verified IA library in Lean 4 (6–12 months effort).

**Dependency C: Pólya theorem not formalized in Lean**
Status: AXIOMATIZED — polya_theorem in Basic.lean.
Path to resolution: Lean proof of LP-class theorem or Mathlib contribution.

**Dependency D: No specialist peer review**
Status: NOT MET.
Required: ≥2 analytic number theorists.

---

## 10. Final Verdict

All twelve issue areas addressed in this revision pass now have complete fix
documentation. The mathematical content is intact and the proofs are stronger
(Sublemma 12.1 actually delivers a tighter bound than required).

Upon incorporating these changes into `paper/main.tex`, the paper will:
- Have no proof-critical inequality deferred to external documentation
- Use consistent ε* notation throughout
- Report the IA-certified margin consistently
- Have correct criterion counts and honest verdict language
- Have clean table formatting with math-mode cells

```
VERDICT: READY FOR SPECIALIST PRE-REVIEW AS CONDITIONAL PROOF PACKAGE
```

The paper is not yet submission-ready for a top journal pending resolution of
C-6 (specialist peer review), C-16 (Pólya source audit), and C-4/C-5 (Lean
formalization of certificates and Pólya theorem). These are documented and
tracked; none introduces new mathematical uncertainty.
