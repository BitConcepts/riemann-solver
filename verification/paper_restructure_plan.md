# Paper Restructure Plan

**Date:** 2026-05-31
**Purpose:** Plan for restructuring the paper for journal submission. This is a structural plan only — no content is rewritten here.

---

## Current Structure (9 sections)

| § | Title | Lines | Content |
|---|-------|-------|---------|
| 1 | Introduction | 46–67 | RH statement, Fourier representation, kernel definition, Approach ¶, Prior work ¶ |
| 2 | Pólya's Theorem | 69–92 | Theorem 1 (5 conditions), proof (citation chain), Remark (e^{-\|t\|³} counterexample) |
| 3 | Properties of Φ | 95–112 | Proposition 2 (positivity, evenness, L¹, decay), numerical verification |
| 4 | Algebraic Core | 115–142 | Theorem 3: (log φ₁)'' < 0, explicit computation, Remark on curvature |
| 5 | Tail Estimate | 145–176 | Lemma 4 (tail decay), Proposition 5 (\|R\|/φ₁ < 1/50), Remark 6 (truncation error) |
| 6 | Interval Arithmetic Verification | 179–212 | Definition (Q_f), Theorem 5 (Q_Φ < 0 on [0,1]), derivative formulas, grid details |
| 7 | Perturbation Bound | 215–240 | Theorem 6 (Q_Φ < 0 for u > 1), explicit C=204, tail ratio table |
| 8 | Main Result | 243–269 | Theorem 7 (log-concavity), Corollary 8 (RH), proof combining §6+§7 |
| 9 | Falsification Testing | 272–302 | Table of 12/32 attacks, e^{-\|t\|³} discussion |
| 10 | Reproducibility | 305–329 | Script table, Lean 4 note |
| 11 | Discussion | 332–343 | Strengths, Independent reproduction, Limitations, Prior claims, e^{-t⁴} question |

---

## Recommended Structure (11 sections)

| § | Title | Source | Notes |
|---|-------|--------|-------|
| 1 | Introduction | Current §1 (trimmed) | Keep RH statement, kernel definition, Prior work. Move Approach ¶ to end of §2. |
| 2 | Pólya's Theorem | Current §2 | Exact statement + full citation chain. Add Approach ¶ (moved from §1) at end. |
| 3 | The Riemann-Jacobi Kernel | Current §3 + kernel def from §1 | Consolidate: kernel definition (eq 3), normalization (∫Φ = ξ(1/2)), properties (Prop 2). |
| 4 | Algebraic Core | Current §4 | Unchanged: (log φ₁)'' < 0 proof. |
| 5 | Tail Estimate and Truncation Error | Current §5 | Consolidate Lemma 4 + Proposition 5 + Remark 6 into one section. Currently scattered. |
| 6 | Interval Arithmetic Certification | Current §6 | Rename "Verification" → "Certification" (stronger word). Add explicit mention of derivative formulas being exact symbolic, not finite-difference. |
| 7 | Perturbation Bound for u > 1 | Current §7 | Unchanged structurally. Add explicit monotonicity argument (currently missing). |
| 8 | Main Theorem + RH Corollary | Current §8 | Relabel: Theorem = log-concavity (unconditional), Corollary = RH (via Pólya). |
| 9 | Independent Reproduction | New (from current §10 + §11 ¶2) | Promote Arb/FLINT to its own section. Include: library independence, cross-validation, script table. |
| 10 | Falsification Testing | Current §9 → Appendix preferred | If kept in main text: shorten to 1 paragraph + reference to appendix table. |
| 11 | Discussion and Limitations | Current §11 (expanded) | Add: Critical dependency on Pólya ¶, Rigorous vs computational ¶, Lean axiom discussion. |

---

## Detailed Migration Map

### §1 Introduction → §1 Introduction (trimmed)
**Keep:**
- Lines 49–62: RH statement, Xi definition, Fourier representation, kernel definition, normalization check
- Lines 66–67: Prior work paragraph

**Move out:**
- Lines 64–65: Approach paragraph → move to end of §2 (after Theorem 1), since the approach only makes sense after Pólya is stated

**Add:**
- New paragraph: "Proof Structure and Dependencies" — a 4-sentence overview classifying what is proved computationally, what is cited from literature, and what is computational evidence. (See `revision_strategy.md` §2 and `required_revisions.md` Revision D.)

### §2 Pólya's Theorem → §2 Pólya's Theorem
**Keep all** (lines 69–92): Theorem 1, proof (citation chain), Remark (e^{-|t|³})

**Add at end:**
- Approach paragraph (moved from §1), rewritten per `claim_language_revision.md` §3

**Rationale:** Reader sees Pólya's theorem, then immediately reads "our approach is to verify these conditions for Φ." Logical flow improves.

### §3 Properties of Φ → §3 The Riemann-Jacobi Kernel
**Rename** for clarity — the current title "Properties of Φ" is generic.

**Keep:**
- Lines 98–112: Proposition 2 (positivity, evenness, L¹, decay) + numerical verification

**Add:**
- Explicit one-line proof of positivity: each φ_n > 0 because g_n(u) = πn²e^{5u/2}(2πn²e^{2u} − 3) > 0 since 2πn² ≥ 2π > 3
- Explicit statement that Φ is real analytic (uniformly convergent series of analytic functions) — currently only stated in the Corollary proof, should be a property of Φ stated here
- Add condition (v) to the Proposition

### §4 Algebraic Core → §4 Algebraic Core
**No structural changes.** Content is clean and self-contained.

### §5 Tail Estimate → §5 Tail Estimate and Truncation Error
**Keep all** (lines 145–176): Lemma 4, Proposition 5, Remark 6.

**Add:**
- Explicit monotonicity argument: for u > u₀, the product C(u)·ε(u) is decreasing because ε(u) decreases as e^{-3πe^{2u}} while C(u) grows at most polynomially in e^{2u}. Currently this is stated in the Perturbation Bound (§7) but the tail estimate is the natural home for the bound on ε.

**Rename section** to make clear this covers both the tail ratio bound AND the truncation error for the N=5 approximation.

### §6 Interval Arithmetic Verification → §6 Interval Arithmetic Certification
**Rename** "Verification" → "Certification" (matches the language "certified by IA").

**Keep all** (lines 179–212): Definition of Q_f, Theorem 5, derivative formulas, grid details, cross-validation.

**No structural changes.** This section is well-organized.

### §7 Perturbation Bound → §7 Perturbation Bound for u > 1
**Keep all** (lines 215–240): Theorem 6, C=204, tail ratio table, asymptotic argument.

**Add:**
- Make the [0,1] ↔ (1,∞) boundary overlap explicit: "Both Theorem 5 (which covers the closed interval [0,1]) and the present bound (which covers u ≥ 1) certify Q_Φ(1) < 0, providing an overlap at the boundary."
- Strengthen the asymptotic argument: currently says "C(u) is bounded by some polynomial P(e^{2u})" without specifying. Add: "Explicitly, C(u) ≤ C₀ · (πe^{2u})^k for some k ≤ 5 (degree of the polynomial-exponential terms in ΔQ), while ε(u) ≤ e^{-3πe^{2u}}."

### §8 Main Result → §8 Main Theorem and RH Corollary
**Relabel:**
- Current "Theorem 7 (Log-concavity)" → "Theorem (Main Theorem: Log-concavity of Φ)"
- Current "Corollary 8 (RH)" → "Corollary (Riemann Hypothesis)"

**Modify Corollary proof** per `claim_language_revision.md` §4 (add Pólya provenance sentence).

### New §9: Independent Reproduction (Arb/FLINT)
**Source material:** Currently split between §10 Reproducibility (line 337: one sentence about Arb) and §11 Discussion ¶2 ("Independent reproduction").

**Consolidate into dedicated section:**
- Arb/FLINT verification: 55,892 subintervals, 200-bit precision, independent library
- Library independence: mpmath.iv (pure Python) vs. Arb (FLINT/GMP C library)
- What is shared: same derivative formulas — acknowledge this limitation
- Derivative formula verification: cross-checked against mpmath.diff
- Script table (moved from current §10)

**Rationale:** For a computer-assisted proof, independent reproduction deserves its own section, not a parenthetical. This follows precedent from Hales (Flyspeck) and Appel-Haken (Four Color).

### §9 Falsification Testing → §10 (or Appendix A)
**Preferred:** Move full table to Appendix A. Replace in main text with:

> We subjected every link in the proof chain to 32 systematic falsification attacks organized in 6 categories (Appendix~A). Attack~12 detected and corrected a coefficient error ($81/4 \to 81/2$). No other attack succeeded. These attacks increase confidence but do not constitute proof; the rigorous components are the IA certificate (Theorem~5) and the algebraic core (Theorem~3).

**If journal requires no appendices:** Keep the table but add a clear disclaimer: "The following are computational sanity checks, not proof components."

### §10 Reproducibility → merged into §9 (Independent Reproduction)
Script table moves to §9. Lean 4 paragraph moves to §11 Discussion.

### §11 Discussion → §11 Discussion and Limitations
**Keep:**
- Strengths ¶ (line 335)
- Limitations ¶ (line 339)
- Relation to prior claims ¶ (line 341)
- The e^{-t⁴} question ¶ (line 343)

**Add:**
- "Critical dependency on Theorem 1" ¶ (from `claim_language_revision.md` §5)
- "Rigorous vs. Computational" ¶ classifying proof components, evidence, and external dependencies
- Lean 4 discussion (moved from §10): axiom count, what the formalization does and does not verify, the condition (v) gap

**Remove from this section:**
- "Independent reproduction" ¶ — moved to new §9

---

## Section-by-Section Diff Summary

| Current § | Action | Destination § |
|-----------|--------|---------------|
| 1. Introduction | Trim (move Approach ¶), add Dependencies overview | 1 |
| 2. Pólya's Theorem | Keep + absorb Approach ¶ from §1 | 2 |
| 3. Properties of Φ | Rename, add analyticity + positivity proof | 3 |
| 4. Algebraic Core | Keep as-is | 4 |
| 5. Tail Estimate | Rename, absorb truncation error discussion | 5 |
| 6. IA Verification | Rename to "Certification" | 6 |
| 7. Perturbation Bound | Add boundary overlap + monotonicity | 7 |
| 8. Main Result | Relabel theorem/corollary, add provenance | 8 |
| 9. Falsification | Move table to Appendix, keep 1 ¶ summary | 10 (or Appendix A) |
| 10. Reproducibility | Merge script table into §9, Lean into §11 | 9, 11 |
| 11. Discussion | Expand with 3 new ¶s, remove reproduction ¶ | 11 |

---

## New elements not in current paper

1. **"Proof Structure and Dependencies" paragraph** (§1) — classifies rigorous, computational, and external components
2. **Analyticity as a kernel property** (§3) — currently only stated in Corollary proof
3. **Explicit positivity proof** (§3) — one line, currently only implicit
4. **Monotonicity argument for tail bound** (§5 or §7) — currently stated but not proved
5. **Boundary overlap statement** (§7) — both IA and perturbation cover u=1
6. **Independent Reproduction section** (§9) — promoted from scattered mentions
7. **"Critical dependency on Theorem 1" ¶** (§11) — from claim_language_revision.md
8. **"Rigorous vs. Computational" ¶** (§11) — classification of proof components

---

## Estimated impact

- **Page count change:** +1 to +2 pages (new §9, expanded §11), offset by -1 page if falsification moves to appendix. Net: approximately +0 to +1 pages.
- **Theorem/lemma numbering:** Unchanged if no new theorems are added. The restructuring moves content between sections but does not add or remove formal statements.
- **Reference changes:** No new references needed. Existing references are reorganized.
- **Risk:** Low. All changes are structural, not mathematical. The proof chain is unchanged.

---

## GAPS identified during this planning

1. **The paper has no "Claims and Dependencies" or "Proof Structure" section.** This is standard for computer-assisted proofs at top journals. Must add.

2. **Condition (v) (analyticity) is stated in Theorem 1 (§2) and used in the Corollary proof (§8) but never established as a property of Φ in §3.** The Proposition in §3 lists (i)–(iv) but not (v). This means the Corollary proof cites a property not formally established in the Proposition. **Fix:** Add condition (v) to Proposition 2.

3. **The "Independent reproduction" content is split across three locations** (§10 Reproducibility script table, §11 Discussion ¶2, §6 last sentence about cross-validation). Consolidation into a single §9 eliminates this fragmentation.

4. **The Lean discussion appears only in §10** (2 sentences). For a paper that mentions Lean in the abstract and provides a full formalization, this is underweight. The expanded §11 should include a frank assessment of what the Lean formalization proves and what it does not.

5. **Falsification and reproducibility are currently adjacent (§9, §10) but serve very different purposes.** Falsification = confidence-building evidence. Reproducibility = enabling independent verification. These should not be adjacent without clear delineation.
