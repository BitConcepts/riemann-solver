# Deliverable: conditional_consequence_language.md
# Task 9 — Conditional Consequence Language for Appendix A

## Required Changes to Appendix A

Each contextual consequence must be explicitly conditional on the RH corollary.

### (i) Griffin–Ono–Rolen–Zagier

OLD:
> Our result implies a strictly stronger statement: since Ξ has only real zeros...

NEW:
> If Corollary~\ref{thm:rh} is accepted (i.e., conditional on the proof chain in
> Section~\ref{sec:deps}), then since Ξ has only real zeros, the sequence (a_{2k}) lies in
> the Laguerre--Pólya class...

### (ii) De Bruijn–Newman constant

OLD:
> Our result implies Λ ≤ 0.

NEW:
> Conditional on Corollary~\ref{thm:rh}, we have Λ ≤ 0. Together with
> Rodgers--Tao~\cite{rodgers2020} ($\Lambda \geq 0$), this gives $\Lambda = 0$.
> This is a consequence of RH, not an independent argument.

### (iii) CvS spectral framework

Already says "we do not rely on these spectral results" — no change needed.
But add at start: "These results are independent numerical evidence and are not part
of the proof chain."

### AEE score

No change needed — already described as an assessment framework, not a proof claim.

## Acceptance Criterion

✓ "Our result implies" replaced with "Conditional on Corollary X, ..."
✓ No consequence is presented as independently established by this paper.
✓ De Bruijn-Newman conclusion is explicitly labeled as a consequence of RH, not
  an independent proof.
