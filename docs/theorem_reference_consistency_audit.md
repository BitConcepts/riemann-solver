# Deliverable: theorem_reference_consistency_audit.md
# Task 13 — Theorem Reference Consistency Audit

## Current Numbering (LaTeX auto-numbered)

With the current paper structure:
  Thm 1: Pólya 1927
  Lem 2: h_pos_for_nonneg (from Lean remark, not in text)
  Prop 3: Phi properties
  Thm 4: Algebraic Core
  Lem 5: tail_decay
  Prop 6: tail_ratio
  Def 7: log-concavity numerator
  Thm 8: IA verification [0,1]
  Lem 9: Uniform tail bound (Lemma W)
  Thm 10: Extended Certification [1,3]
  Thm 11: Tail Bound [3,inf)
  Thm 12: Main log-concavity result
  Cor 13: RH Corollary

These are automatically assigned by LaTeX. The paper refers to them only by
\ref{} labels, so no manual number tracking is needed.

## Stale references to fix in paper

1. Abstract: "Theorem~5 in Section~\ref{sec:extended}" should just be
   "Theorem~\ref{thm:extended} in Section~\ref{sec:extended}" — already fixed.

2. Section 12 (Reproducibility): 
   "\texttt{proof/verify\_ia\_1\_to\_1\_5.py}" → "\texttt{proof/verify\_ia\_1\_to\_3.py}"
   "\texttt{results/verify\_ia\_1\_to\_1\_5.json}" → "\texttt{results/verify\_ia\_1\_to\_3.json}"

3. Lean axiom name: "\texttt{ia\_verification\_1\_0\_to\_1\_5}" should still be
   updated to reflect [1,3] coverage in the next Lean revision.

4. Appendix B: C5 row should reference verify_ia_1_to_3.py and new hash.
