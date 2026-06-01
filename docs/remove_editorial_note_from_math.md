# Deliverable: remove_editorial_note_from_math.md

## Problem
Theorem 5 proof contains inside a displayed equation:
  \varepsilon^*(u) := 2\sum ... \quad\text{[corrected: }B_n(u)/n^4 < 2\text{]},

The bracketed editorial note should NOT appear inside the displayed math.

## Fix
Move the note to prose after the display:
  \varepsilon^*(u) := 2\sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}},

Then add prose: "The factor~2 is the corrected prefactor bound established in 
Proposition~\ref{prop:tail_ratio}: $B_n(u)/n^4 \leq 1 + 3/(2\pi-3) < 2$."
