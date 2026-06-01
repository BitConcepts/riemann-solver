# Deliverable: qed_symbol_layout_fix.md
# Task 11 — Fix QED Symbol Placement

## Problem

In Theorem 6 proof, the SHA256 hash reference appears at the end of the proof,
causing the QED square to appear awkwardly after code text.

## Fix

Remove the SHA256 parenthetical from the Theorem 6 proof body.
The hash belongs in Appendix B only.

In Theorem 6 proof, change:
  "See \texttt{proof/verify\_algebraic\_core.py} (SHA256 of output: \texttt{7D65253C...})."
To:
  "See \texttt{proof/verify\_algebraic\_core.py}."

In Theorem 5 proof, similarly remove the inline SHA reference:
  "See \texttt{proof/verify\_ia\_1\_to\_3.py} (SHA256 of output: \texttt{7D65253C...})."
To:
  "See \texttt{proof/verify\_ia\_1\_to\_3.py} and Appendix~\ref{sec:cert}."

The QED marker will then appear cleanly after a mathematical sentence.
