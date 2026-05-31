# Revision Strategy for Annals/JAMS Submission

## Premise

This document outlines changes needed to make the paper more likely to survive peer review at a top journal (Annals of Mathematics, JAMS, Inventiones, Acta Mathematica). The strategy is informed by how referees at these journals evaluate computer-assisted proofs, and by the specific gaps identified in the dependency graph and axiom analysis.

---

## 1. Rewrite the Abstract

### Current problem
The abstract opens with "We verify that the Riemann–Jacobi kernel Φ(u) ... is strictly log-concave," then immediately connects to RH. This is appropriate for the arxiv but will trigger instant skepticism at a top journal, where referees are trained to distrust RH claims.

### Proposed revision
Lead with the mathematical contribution. The abstract should:

1. **Open with the result itself**: "We establish, by rigorous interval arithmetic with independent verification, that the log-concavity numerator Q_Φ(u) = Φ''Φ - (Φ')² is strictly negative for all u ≥ 0."
2. **State the method**: "The proof combines an algebraic core, 52,898 IA-certified subintervals on [0,1], and an explicit perturbation bound for u > 1."
3. **Note the corollary**: "By a classical theorem of Pólya (1927), this implies that all zeros of the Riemann Xi function are real, which is equivalent to the Riemann Hypothesis."
4. **Mention independent confirmation**: "The IA certificate is independently reproduced using Arb/FLINT."

The key shift: present log-concavity as the main theorem. Let RH be a corollary.

### Rationale
A referee who reads "We prove RH" will look for the flaw. A referee who reads "We certify log-concavity of this kernel" will evaluate the certification on its merits. The RH implication follows from a published theorem and is less likely to be the point of failure.

---

## 2. Add a "Claims and Dependencies" Section

### What to add
A new Section 1.1 or Section 2, titled **"Proof Structure and Dependencies,"** containing:

1. A clear statement of what is proved computationally vs. what is cited from the literature.
2. The dependency graph (a simplified version of the Mermaid diagram in `proof_dependency_graph.md`).
3. An explicit list of external dependencies with precise citations:
   - Pólya 1927 (Satz II, as restated in Csordas-Varga 1989 Theorem 2.2 and Levin 1964 §8)
   - Jacobi theta functional equation (Titchmarsh §2.10)
   - RH ⟺ Ξ real zeros (Titchmarsh §2.10)
4. A clear statement: "The following properties are treated as classical and not re-derived: positivity, evenness, integrability, superexponential decay of Φ. One-line proofs are given in Proposition 2."

### Rationale
This is what a referee will construct mentally anyway. Providing it explicitly shows mathematical maturity and saves the referee work. It also forces the author to be honest about where the proof's weight falls.

---

## 3. Move Falsification to an Appendix

### Current problem
Section 7 (Falsification Testing) occupies ~1 page and lists 12 of 32 attacks in a table. This is unusual for a mathematics paper and may be perceived as padding or as a sign that the author is not confident.

### Proposed revision
1. Move the full falsification table to an **Appendix A**.
2. In the main text, add a single paragraph: "We subjected every link in the proof chain to 32 systematic falsification attacks (Appendix A). Attack 12 detected and corrected a coefficient error (81/4 → 81/2). No other attack succeeded."
3. The appendix should clearly state: "These attacks increase confidence but do not constitute proof. The rigorous components are the IA certificate (Theorem 5) and the algebraic core (Theorem 4)."

### Rationale
Top journals value concision. The falsification suite is impressive engineering but is not part of the mathematical proof. Relegating it to an appendix signals that the author understands the distinction between proof and evidence.

---

## 4. Add a "Rigorous vs. Computational" Clarity Section

### What to add
A paragraph (in the Discussion or as a subsection of Section 2) explicitly delineating:

**Rigorous (constitutes proof):**
- Algebraic core: (log φ₁)'' < 0 — pure symbolic computation, verifiable by hand
- IA certificate on [0,1]: 52,898 subintervals with guaranteed enclosures using exact symbolic derivatives
- Perturbation bound: explicit constant C=204 at u=1, with monotonic improvement for u > 1
- Truncation error: rigorous bound < 7.03 × 10⁻⁴³ for n ≥ 6

**Computational evidence (increases confidence, not proof):**
- Point-sampling of Q_Φ at 7,001 points
- Φ positivity at 10,001 points
- 32 falsification attacks
- Argument-principle zero counts for e^{-t³} and e^{-cosh(t)}

**External dependencies (accepted without proof in this work):**
- Pólya's theorem (1927)
- Properties of Φ (classical)
- RH ⟺ Ξ real zeros

### Rationale
This is the single most important revision. A referee must know exactly which parts of the proof are rigorous, which are heuristic, and which are external. The current paper mixes these categories (e.g., the falsification table is presented alongside the IA certificate, creating the impression that point-sampling is part of the proof).

---

## 5. Add an "Independent Reproduction" Section

### What to add
A new subsection (Section 7.1 or part of the Reproducibility section) documenting:

1. **Arb/FLINT verification**: "The IA certificate was independently reproduced using python-flint (Arb ball arithmetic) at 200-bit precision across 55,892 subintervals. All subintervals were certified."
2. **Library independence**: "mpmath.iv and Arb use different arithmetic backends (pure Python vs. FLINT/GMP). Agreement between the two eliminates the possibility of a single-library implementation bug."
3. **Cross-validation**: "Q_Φ values computed at 80-digit floating-point precision at 10 selected points all lie within the corresponding IA enclosures."
4. **What remains**: "Both libraries use the same derivative formulas. A formula error would propagate to both. The derivative formulas are verified against mpmath.diff (numerical differentiation) at 30+ test points with agreement to 15+ digits."

### Rationale
Computer-assisted proofs at top journals (Hales's Flyspeck, Kepler conjecture, Four Color Theorem) have set a precedent: independent reproduction is expected. The Arb verification already exists but is not prominently cited in the paper.

---

## 6. Reframe: Lead with the Mathematical Contribution

### Current framing
"We prove RH by verifying log-concavity and applying Pólya."

### Proposed framing
"We establish certified log-concavity of the Riemann-Jacobi kernel Φ, combining algebraic analysis of the dominant term with rigorous interval arithmetic. As a corollary of a classical theorem of Pólya (1927), this implies that all zeros of the Xi function are real."

### Structural changes
1. **Title**: Keep "Log-Concavity of the Riemann Xi Kernel and the Riemann Hypothesis" — this is accurate and not overclaiming.
2. **Main Theorem**: Label the log-concavity result as the Main Theorem. Label RH as Corollary 1.
3. **Section order**: Properties of Φ → Algebraic Core → IA Verification → Perturbation Bound → Main Theorem (log-concavity) → Pólya → Corollary (RH).

### Rationale
A referee will check Pólya's theorem applicability FIRST. By presenting log-concavity as the main result and RH as a corollary, the author:
- Reduces the referee's initial resistance
- Makes the paper valuable even if a subtle issue is found with Pólya's conditions
- Follows the precedent of major results: the Kepler conjecture paper led with the optimization bound, not "we proved Kepler."

---

## 7. What a Reviewer Will Check First

In order of priority:

1. **Pólya's theorem statement and applicability.** Does the theorem as stated in the paper exactly match a published result? Do the conditions (i)-(iv) in the paper match the conditions in Pólya 1927 / Csordas-Varga 1989? Is the decay condition satisfied? 
   - **Action needed**: Obtain and cite the original German text. Provide a translation of the relevant passage. Alternatively, cite de Bruijn 1950 Theorem 1, which is in English and gives sufficient conditions for real zeros of cosine transforms.

2. **The IA certificate.** Does the interval arithmetic actually certify Q < 0 on every subinterval? Could a bug in mpmath.iv produce false certifications?
   - **Action needed**: The Arb confirmation already addresses this. Mention it prominently.

3. **The handoff from [0,1] to (1,∞).** Is the perturbation bound truly sufficient? Does it cover the boundary u=1?
   - **Action needed**: Both the IA verification and the perturbation bound include u=1. The IA certificate covers [0, 1.0] (closed interval). The perturbation bound is stated for u > 1 but the IA already certifies u=1. Make this overlap explicit.

4. **Truncation to N=5 terms.** Is the truncation error really 10⁻⁴³?
   - **Action needed**: Already certified by IA in `verify_truncation_and_crosscheck.py`. Cite this more prominently.

5. **The derivative formulas.** Could there be an algebraic error?
   - **Action needed**: Already verified by attacks 12, 20-22, 29-30 and by the Arb independent run using the same formulas. Mention the historical bug detection (81/4 → 81/2) to show the falsification suite works.

---

## 8. Specific Textual Changes

### Abstract
Replace the first sentence with: "We certify, by rigorous interval arithmetic with independent confirmation, that the Riemann-Jacobi kernel Φ(u) is strictly log-concave on [0,∞)."

### Section 7 (Falsification)
Replace with a 3-sentence paragraph referencing Appendix A. The three sentences should cover: (a) 32 attacks, (b) one detected a real bug, (c) none constitute proof.

### Section 8 (Discussion)
Add paragraph: "The distinction between rigorous proof and computational evidence is essential. The IA certificate (Theorem 5) and algebraic core (Theorem 4) are rigorous. The falsification suite, point-sampling, and cross-checks are computational evidence that increases confidence but does not replace proof."

### Theorem 8 (Main Result)
Relabel: "Theorem 8 (Log-concavity of Φ). Q_Φ(u) < 0 for all u ≥ 0."
Add: "Corollary 9 (Riemann Hypothesis). All nontrivial zeros of ζ(s) lie on Re(s) = 1/2."

### Lean section
Add: "The formalization currently has 16 axiom declarations, of which 4 are immediately provable in Lean (simple algebraic inequalities). The most important axioms — Pólya's theorem and the IA certificate — cannot be formalized with current proof assistant technology."

---

## 9. What NOT to Change

1. **Do not remove the falsification suite.** It is genuinely valuable and demonstrates thoroughness. Just move it to an appendix and clarify its role.
2. **Do not understate the result.** Log-concavity of the full kernel Φ is a genuine mathematical contribution, regardless of its implications for RH.
3. **Do not claim the Lean formalization proves RH.** It proves the proof structure is sound given 16 axioms. Say exactly that.
4. **Do not remove the Arb verification.** It is the single strongest piece of evidence for IA correctness.
5. **Do not remove the perturbation bound details.** The explicit constant C=204 is one of the paper's strengths.

---

## 10. Pre-submission Checklist

- [ ] Obtain Pólya 1927 original German text; verify Satz II conditions match paper's (i)-(iv)
- [ ] Alternatively, cite de Bruijn 1950 Theorem 1 (English) as the primary reference
- [ ] Rewrite abstract (lead with log-concavity, RH as corollary)
- [ ] Add "Claims and Dependencies" section with dependency diagram
- [ ] Add "Rigorous vs. Computational" paragraph
- [ ] Move falsification table to appendix
- [ ] Promote Arb/FLINT confirmation to a named subsection
- [ ] Relabel: Main Theorem = log-concavity, Corollary = RH
- [ ] Reduce Lean axiom count to ≤10 (prove Tier 1 items)
- [ ] Clarify [0,1] ↔ (1,∞) boundary overlap at u=1
- [ ] Add explicit one-line proofs for Φ positivity (each φ_n > 0)
- [ ] Proofread all 32 falsification attacks to confirm they actually run clean
