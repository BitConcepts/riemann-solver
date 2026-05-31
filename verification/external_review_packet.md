# External Review Packet

**Date:** 2026-05-31
**Purpose:** Materials for soliciting expert review of the log-concavity RH proof. Four reviewer profiles with targeted questions and a one-page proof summary for initial outreach.

---

## One-Page Proof Summary (for emailing potential reviewers)

> **Title:** Log-Concavity of the Riemann Xi Kernel and the Riemann Hypothesis
>
> **Author:** Tristen Kyle Pierson, BitConcepts Research
>
> **Repository:** https://github.com/BitConcepts/riemann-solver
>
> **Summary:** We certify that the Riemann–Jacobi kernel Φ(u), appearing in the Fourier cosine representation Ξ(t) = ∫₀^∞ Φ(u)cos(tu) du, is strictly log-concave on [0,∞). The kernel is Φ(u) = 4 Σ φₙ(u), where φₙ(u) = (2π²n⁴e^{9u/2} − 3πn²e^{5u/2})e^{−πn²e^{2u}}. Log-concavity is established by proving the numerator Q_Φ(u) = Φ''Φ − (Φ')² < 0 everywhere.
>
> **Method:** Three components:
> 1. *Algebraic core:* (log φ₁)''(u) < 0 for all u ≥ 0, by explicit computation (sum of two negative terms).
> 2. *Interval arithmetic on [0,1]:* 52,898 subintervals at 60-digit precision certify Q_Φ < 0, using N=5 terms with truncation error < 7.03×10⁻⁴³. Independently reproduced using Arb/FLINT (55,892 subintervals, 200-bit precision).
> 3. *Perturbation bound for u > 1:* The tail R = Σ_{n≥2} φₙ satisfies |R|/φ₁ < 10⁻²⁹ at u=1, with explicit constant C=204, so the perturbation cannot flip the sign of Q_{φ₁}.
>
> **RH implication:** By Pólya's 1927 theorem (Satz II), a kernel that is even, positive, L¹, log-concave, real analytic, and superexponentially decaying has a cosine transform with only real zeros. Φ satisfies all conditions. Since RH ⟺ all zeros of Ξ are real, the Riemann Hypothesis follows.
>
> **Key dependency:** The inference from log-concavity to RH rests entirely on Pólya's theorem, cited from secondary sources (Csordas–Varga 1989, Levin 1964, de Bruijn 1950). The original German text has not been independently translated.
>
> **Verification artifacts:** Python scripts (mpmath.iv + python-flint), Lean 4 formalization (16 axioms, 0 sorry), 32-attack falsification suite, JSON certificate.
>
> **What we ask you to check:** [Customize per reviewer profile below.]

---

## Reviewer A: Entire Functions / Laguerre–Pólya Class Expert

### What to check
Reviewer A should verify the exact statement and applicability of Pólya's 1927 theorem (Satz II) as used in the paper. This is the single most critical external dependency. The reviewer should confirm that the five conditions stated in Theorem 1 (positivity, L¹, log-concavity, superexponential decay, real analyticity near the origin) are sufficient for the conclusion that the cosine transform has only real zeros, and that these conditions match Pólya's original result as understood in the Laguerre–Pólya literature. The reviewer should also assess whether the e^{−|t|³} counterexample is correctly analyzed and whether it establishes the sharpness of condition (v).

### Specific questions
1. Does the five-condition version of Pólya's theorem in Theorem 1 faithfully represent Satz II of Pólya (1927)? If not, what is the correct statement?
2. Is condition (v) (real analyticity near the origin) actually required by Pólya, or is it an artifact of the Csordas–Varga restatement? Could a weaker regularity condition (e.g., C^∞) suffice?
3. The function e^{−|t|³} satisfies conditions (i)–(iv) but fails (v). The paper claims its cosine transform has complex zeros (4 found by argument principle in [5,15]×[−5,5]). Is this consistent with the known literature on entire functions of order 3?
4. Is the paper's claim that Φ is real analytic (as a uniformly convergent series of analytic functions) sufficient, or does one need to verify convergence in a complex strip?
5. Does the paper's kernel Φ lie in the class S (i.e., ∫e^{bt²}Φ(t)dt < ∞ for all b > 0)? If so, does membership in S alone suffice for the Pólya conclusion, bypassing the need for condition (v)?
6. The de Bruijn–Newman constant Λ = 0 (Rodgers–Tao 2020). If log-concavity of Φ is established, does this give an independent proof that Λ ≤ 0? Is this consistent with the Rodgers–Tao result?
7. Michałowski (2026) showed Φ is not PF₅. Does this have any implications for the applicability of Pólya's theorem (which only requires PF₂ / log-concavity)?

### Files and sections to focus on
- `paper/main.tex` §2 (lines 69–92): Theorem 1 statement, proof, and Remark
- `paper/main.tex` §8 (lines 254–269): Corollary proof (conditions checklist)
- `paper/references.bib`: entries for polya1927, csordas1989, levin1964, debruijn1950
- `verification/polya_theorem_audit.md`: detailed cross-reference of secondary sources
- `verification/polya_theorem_red_alert_audit.md`: analysis of the e^{−|t|³} tension
- `verification/decay_counterexample_clarification.md`: e^{−|t|³} analysis
- `falsification/`: Attack 1 (e^{−t³} complex zeros) and Attack 27 (e^{−cosh(t)})

### Known risks to flag proactively
- **The original German text of Satz II has not been independently read.** The paper relies on Csordas–Varga (1989) and Levin (1964) as English restatements. These are standard references (~60 citing papers) but are secondary.
- **The paper initially omitted condition (v).** It was added after the e^{−|t|³} analysis revealed a counterexample to the four-condition version. The fix is correct but the history suggests the author was not initially aware of this subtlety.
- **Condition numbering mismatch:** Theorem 1 lists (i)–(v), but the Corollary proof lists (i)–(vi) with different numbering. This is confusing but not mathematically erroneous.

---

## Reviewer B: Analytic Number Theorist

### What to check
Reviewer B should verify the identity and normalization of the Riemann–Jacobi kernel Φ, confirm that the cosine representation Ξ(t) = ∫Φ(u)cos(tu)du is correct with the stated formula for φₙ, and confirm that RH is equivalent to Ξ having only real zeros. The reviewer should also check the algebraic core (§4) for correctness — this is elementary but is the only purely mathematical proof in the paper.

### Specific questions
1. Is the kernel formula Φ(u) = 4 Σ (2π²n⁴e^{9u/2} − 3πn²e^{5u/2})e^{−πn²e^{2u}} correct? Does it match the standard derivation from Jacobi's theta function via ξ(s) = (1/2)s(s−1)π^{−s/2}Γ(s/2)ζ(s)?
2. The paper verifies ∫₀^∞ Φ(u)du = ξ(1/2) ≈ 0.4971 numerically. Is this the expected normalization? Some references use Φ without the factor of 4, or define ξ differently.
3. In the algebraic core (§4), the proof writes log φ₁ = log π + (5/2)u + log h(u) − πe^{2u}, then computes (log φ₁)'' = (log h)'' − 4πe^{2u}. Is this correct? In particular, is the term (5/2)u handled correctly (its second derivative is 0)?
4. The derivative formulas for g_n', g_n'', E_n', E_n'' (§6, lines 201–206) are used for all IA computations. Are these correct? In particular, is g₁'' = (81/2)π²e^{9u/2} − (75/4)πe^{5u/2}? (The coefficient 81/2 was historically wrong as 81/4 and was caught by falsification attack 12.)
5. Does the evenness Φ(−u) = Φ(u) follow from the Jacobi theta functional equation? Which form of the functional equation is used?
6. Is the decay Φ(u) = O(e^{−πe^{2u}}) correct as u → +∞? Is the dominant term φ₁ or does any subtlety arise from cancellations?

### Files and sections to focus on
- `paper/main.tex` §1 (lines 49–62): kernel definition and normalization
- `paper/main.tex` §3 (lines 95–112): Proposition 2 (kernel properties)
- `paper/main.tex` §4 (lines 115–142): Algebraic Core proof
- `paper/main.tex` §6 (lines 196–206): derivative formulas
- `verification/kernel_normalization_audit.md`: detailed normalization check
- `verification/xi_kernel_normalization_audit.md`: cross-reference with Titchmarsh
- `verification/algebraic_core_verification.md`: algebraic core audit
- `proof/verify_algebraic_core.py`: computational verification of algebraic core

### Known risks to flag proactively
- **Convention variation:** The factor of 4 in Φ = 4Σφₙ differs from some references. The paper's ∫Φ du = ξ(1/2) check confirms the convention, but a reviewer should verify.
- **Historical bug in g'':** The coefficient was 81/4 instead of 81/2. This was caught by attack 12 and fixed. The current formulas are correct but the reviewer should independently verify (9/2)² × 2 = 81/2.
- **The proof of (log φ₁)'' < 0 is the only purely mathematical argument.** Everything else is either classical, computational, or external. This proof is elementary (4 lines) but must be correct.

---

## Reviewer C: Validated Numerics / Interval Arithmetic Expert

### What to check
Reviewer C should verify the correctness and rigor of the interval arithmetic certification: that mpmath.iv (and independently Arb/FLINT) correctly certify Q_Φ < 0 on all 52,898 (resp. 55,892) subintervals, that the truncation error bound is valid, that the derivative formulas used in the IA computations are correct, and that the grid refinement strategy near u=1 (where Q_Φ is small) is adequate.

### Specific questions
1. Does mpmath.iv provide guaranteed enclosures for the operations used (exp, multiplication, addition)? Are there known bugs in mpmath.iv's interval arithmetic that could produce false negatives (i.e., claim an interval is negative when it contains zero)?
2. The grid uses 1,898 subintervals on [0, 0.949] and 51,000 on [0.949, 1.0]. Is this refinement justified? What is the minimum |Q_Φ| on the coarsest subintervals, and is it well-separated from the truncation error?
3. The truncation error bound claims |δ| ≤ 7.03×10⁻⁴³ for the n≥6 omission. How is this bound derived? Is it computed by IA or by analytic bounding?
4. The propagated Q error is bounded by 1.15×10⁻⁴². The derivation uses Q_Φ = Q_{Φ₅} + (Φ₅''δ + δ''Φ₅ − 2Φ₅'δ') + (δ''δ − (δ')²). Are the cross terms correctly bounded? Is the worst case at u=1 correctly identified?
5. The Arb/FLINT verification uses 200-bit precision and a different grid (split at u=0.946 instead of 0.949). Do both verifications cover the same domain [0,1]? Do the enclosures overlap at the grid boundaries?
6. The cross-validation checks that 80-digit float values lie within IA enclosures at 10 points. Is this a meaningful check? Could a systematic error (e.g., wrong formula) pass this test?
7. The derivative formulas are "exact symbolic" — they are closed-form expressions, not finite differences. But they are evaluated in interval arithmetic. Is there any concern about catastrophic cancellation in the IA evaluation of Q_Φ = Φ''Φ − (Φ')²?
8. At u=1, the minimum |Q_{Φ₅}| is 3.36×10⁻¹². With 60-digit (≈200-bit) precision, is this safely above the rounding threshold of the IA implementation?

### Files and sections to focus on
- `paper/main.tex` §6 (lines 179–212): IA verification details
- `paper/main.tex` §5, Remark 6 (lines 164–176): truncation error analysis
- `proof/verify_logconcavity_rigorous.py`: primary IA certification script (mpmath.iv)
- `proof/verify_logconcavity_arb.py`: independent Arb/FLINT reproduction
- `proof/verify_truncation_and_crosscheck.py`: truncation error certification
- `verification/interval_reproduction_report.md`: Arb vs mpmath comparison
- `verification/truncation_error_audit.md`: truncation error audit
- `verification/truncation_error_verification.md`: detailed truncation verification
- `verification/certificate_checker_audit.md`: certificate format and verification
- `verification/certificate.json`: the actual IA certificate
- `verification/verify_certificate.py`: standalone certificate verifier

### Known risks to flag proactively
- **mpmath.iv is a pure-Python implementation.** It is not as widely audited as Arb/FLINT (which is a C library with extensive testing). The Arb reproduction mitigates this, but a reviewer should be aware.
- **Both IA implementations use the same derivative formulas.** A formula error would propagate to both. The formulas are cross-checked against mpmath.diff (numerical differentiation), but this is a finite-precision check, not a proof.
- **Near u=1, Q_Φ ≈ −3.36×10⁻¹².** This is small relative to the individual terms Φ''Φ and (Φ')², which are O(10⁻⁶). Catastrophic cancellation is possible in floating-point but should be handled correctly by IA (which tracks error bounds). The reviewer should verify this.
- **The certificate is a JSON file** containing interval endpoints for each subinterval. The standalone verifier (`verify_certificate.py`) re-checks each interval. The reviewer should run this verifier independently.
- **The paper claims "60-digit precision"** but mpmath.iv actually uses binary precision internally. 60 decimal digits ≈ 200 binary bits. The reviewer should confirm that the precision setting is sufficient.

---

## Reviewer D: Formal Methods / Lean Expert

### What to check
Reviewer D should verify the Lean 4 formalization: that the axioms are reasonable, that the proof structure is sound, that no `sorry` declarations are hidden, and that the axiom interface correctly captures the mathematical claims. The reviewer should also assess what the formalization does and does not prove, and whether the axiom count (16) is appropriate.

### Specific questions
1. The Lean file has 16 axiom declarations. Are any of these trivially provable in Lean (with or without Mathlib)? Which axioms could be reduced?
2. The axiom `polya_theorem` currently takes hypotheses for positivity, evenness, integrability, log-concavity, and superexponential decay but **omits real analyticity** (condition (v) of Theorem 1 in the paper). This means the Lean formalization would accept e^{−|t|³} as a valid kernel, which is a known counterexample. Is this a critical gap?
3. Are the `Prop` types semantically meaningful? For example, `phi_positive : Prop` does not encode the mathematical content "Φ(u) > 0 for all u" — it is an opaque proposition. Does this limit what the formalization actually verifies?
4. The theorem `riemann_hypothesis` is proved by chaining axioms: `polya_theorem` → `xi_real_zeros` → `rh_equivalence`. Is this chain correct? Are there any circular dependencies?
5. Does `autoImplicit = false` eliminate all implicit argument issues?
6. The Lean file compiles with zero `sorry`. Is there any way to achieve "zero sorry" while still having gaps (e.g., through `axiom` declarations that are never discharged)?
7. Could the formalization be strengthened by proving Tier 1 algebraic axioms (e.g., `h_pos_for_nonneg`: 2π > 3) within Lean, rather than axiomatizing them?
8. The header comment claims tier counts (Tier 1: 6, Tier 2: 3, etc.) that may not match the actual code. Does the code match the header?

### Files and sections to focus on
- `lean4/RHProof/Basic.lean`: the complete Lean formalization
- `paper/main.tex` §10 (lines 329–330): Lean discussion in paper
- `verification/lean_formalization_audit.md`: detailed Lean audit
- `verification/lean_axiom_reduction_report.md`: which axioms could be proved
- `verification/certificate_schema.md`: certificate interface between computation and Lean

### Known risks to flag proactively
- **The Lean formalization is axiom-heavy by design.** It axiomatizes computational results (IA certificate, derivative formulas) because current proof assistants cannot efficiently verify interval arithmetic computations. This is a deliberate design choice, not a bug, but it means the Lean proof is a structural check, not an independent verification.
- **The missing `phi_real_analytic` axiom is a genuine gap.** The Lean proof is valid for kernels that don't satisfy condition (v), which means it would "prove" RH for the e^{−|t|³} kernel — a known counterexample. This must be fixed before submission.
- **The `Prop` types carry no mathematical content.** `phi_positive`, `phi_even`, etc. are opaque propositions. The Lean proof verifies that the logical structure is correct (given these propositions, RH follows), but it does not verify that these propositions are true. This is acknowledged in the paper but should be stated more explicitly.
- **Tier count errors in the header comment** have been identified. These are cosmetic but erode confidence in a formalization file.
- **The certificate interface** — how computational results are imported into the Lean proof — is via axioms. A stronger approach would be to have the IA computation produce a Lean-checkable proof term, but this is beyond current technology for 60-digit interval arithmetic.

---

## Review Coordination Notes

### Suggested review order
1. **Reviewer A first** — if Pólya's theorem does not apply, the rest is moot.
2. **Reviewer B second** — if the kernel identity is wrong, the computation is meaningless.
3. **Reviewer C third** — validates the computational core.
4. **Reviewer D fourth** — assesses the formal verification layer.

### Cross-reviewer dependencies
- Reviewer A's assessment of Pólya's conditions determines whether Reviewer B needs to verify condition (v) (analyticity) for Φ.
- Reviewer B's verification of the kernel formula determines whether Reviewer C's IA verification is computing the right thing.
- Reviewer C's assessment of the IA certificate determines whether Reviewer D's Lean axioms for `ia_certificate_01` are grounded.

### What constitutes a fatal finding
- Reviewer A finds that Pólya's theorem requires a condition that Φ does not satisfy → **fatal**
- Reviewer B finds the kernel formula is wrong → **fatal** (but easily checked numerically)
- Reviewer C finds the IA certification has a systematic error → **fatal** (but mitigated by two independent libraries)
- Reviewer D finds a logical gap in the Lean proof → **moderate** (Lean is supplementary, not the main proof)

### What constitutes a non-fatal but important finding
- Reviewer A finds the exact Pólya conditions are slightly different but Φ still satisfies them → **revise paper, not fatal**
- Reviewer C finds the truncation error bound is wrong but the safety factor is large enough to absorb the correction → **revise bound, not fatal**
- Reviewer D finds the `phi_real_analytic` gap → **fix the axiom, not fatal** (already flagged)

---

## Appendix: Complete file inventory for reviewers

### Core paper
- `paper/main.tex` — LaTeX source (349 lines)
- `paper/references.bib` — bibliography
- `paper/Pierson_2026_LogConcavity_RH.pdf` — compiled PDF

### Proof scripts
- `proof/verify_logconcavity_rigorous.py` — primary IA certification (mpmath.iv)
- `proof/verify_logconcavity_arb.py` — independent Arb/FLINT reproduction
- `proof/verify_algebraic_core.py` — algebraic core verification
- `proof/verify_truncation_and_crosscheck.py` — truncation error + cross-validation
- `proof/verify_debruijn_condition.py` — de Bruijn condition check

### Falsification
- `falsify.py` — 32-attack falsification suite
- `falsification/` — individual attack scripts

### Formal verification
- `lean4/RHProof/Basic.lean` — Lean 4 formalization

### Verification documents (this directory)
- `polya_theorem_audit.md` — Pólya theorem cross-reference
- `polya_theorem_red_alert_audit.md` — e^{−|t|³} tension analysis
- `algebraic_core_verification.md` — algebraic core audit
- `kernel_normalization_audit.md` — kernel formula check
- `interval_reproduction_report.md` — mpmath vs Arb comparison
- `truncation_error_audit.md` — truncation error analysis
- `lean_formalization_audit.md` — Lean code audit
- `lean_axiom_reduction_report.md` — axiom reduction plan
- `proof_dependency_graph.md` — full dependency graph
- `final_audit_report.md` — consolidated audit findings
- `certificate.json` — IA certificate
- `verify_certificate.py` — standalone certificate verifier

### Entry points for each reviewer
- **Reviewer A:** Start with `paper/main.tex` §2, then `polya_theorem_audit.md`
- **Reviewer B:** Start with `paper/main.tex` §1 + §4, then `kernel_normalization_audit.md`
- **Reviewer C:** Start with `proof/verify_logconcavity_rigorous.py`, then `interval_reproduction_report.md`
- **Reviewer D:** Start with `lean4/RHProof/Basic.lean`, then `lean_formalization_audit.md`
