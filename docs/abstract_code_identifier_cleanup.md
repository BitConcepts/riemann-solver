# Deliverable: abstract_code_identifier_cleanup.md
# Task 15 — Remove Code Identifiers from Abstract

## Required removals from abstract

Remove all of the following from the abstract (move to Section 12):
- "\texttt{lean4/RHProof/Basic.lean}"
- "\texttt{lake build}"
- "leanprover/lean4:v4.16.0"
- "Mathlib commit \texttt{a6276f4c}"
- "\texttt{h\_pos\_for\_nonneg}, \texttt{log\_h\_d2\_neg}, ..."
- "13 project-specific axioms"
- "3 universal Lean kernel axioms"
- "\texttt{propext}, \texttt{Classical.choice}, \texttt{Quot.sound}"

Replace with:
"A Lean 4 formalization verifies the algebraic core with zero \texttt{sorry}
declarations; remaining dependencies are recorded as explicit axioms."

This is already handled in the shortened abstract (Task 6).
