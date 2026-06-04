# Bridge Status Matrix

Tracks all candidate theorem bridges. Updated after every research iteration.

**Last updated:** 2026-06-04 (initial setup)

---

## Status codes

- OPEN — not yet resolved; no theorem found
- POSSIBLE — candidate theorem identified; hypotheses not yet fully matched
- PARTIAL — theorem found; applies to Φ conditionally, with remaining gap
- REJECT — theorem requires circular assumption or does not apply to Φ
- PROMOTED — hypotheses matched; theorem provides valid bridge (update immediately if reached)

---

## Candidate matrix

| Candidate theorem | Source | Hypotheses | Conclusion | Applies to Φ? | Gap | Status |
|---|---|---|---|---|---|---|
| H13 (strong log-concavity) | Unsourced | even + positive + integrable + analytic + superexp decay + log-concave | Fourier has only real zeros | Yes (if true) | Theorem not proved or sourced | OPEN |
| Pólya Satz I | Pólya 1927 | Prior real-rooted Fourier + LP multiplier | Preserves real zeros | No — circular | Requires prior real-rootedness | REJECT |
| Pólya Satz II | Pólya 1927 | Mellin transform has negative real zeros | Fourier has real zeros | Conditional | Mellin zero structure of Φ unverified | PARTIAL |
| Csordas–Varga Thm 2.2 | Csordas–Varga 1989 | Mellin condition (restates Pólya Satz II) | Fourier has real zeros | Conditional | Same as Pólya Satz II | PARTIAL |
| de Bruijn (1950) main thm | de Bruijn 1950 | LP condition on derivative | Fourier has real zeros | Unknown | LP condition stronger than log-concavity | PARTIAL |
| Csordas-Vishnyakova Thm 2.3 | Csordas-Vishnyakova 2013 | ALL $L_n \geq 0$ for all $n$, all $x$ | $\phi \in L$-$P$ (real zeros) | PARTIAL | Only $L_1$ proved for $\Phi$; need all orders | PARTIAL MATCH |
| Cardon 2002 Theorem 1 | Cardon 2002 | $G$ already in LP class | Convolution preserves real zeros | No | Circular: G must already have real zeros | REJECT |
| Pólya Hilfssatz II | Pólya 1927 (via Cardon 2002) | $G$ already has only real zeros | $G(z+ia)+G(z-ia)$ has real zeros | No | Circular: requires prior real-rootedness | REJECT |
| Cardon 2005 Fourier paper | Cardon 2005 | TBD | TBD | TBD | Not yet acquired | POSSIBLE |
| Cardon 2009 Extended Laguerre | Cardon 2009 | Extended Laguerre ineqs? | Real zeros criterion? | TBD | Not yet acquired | POSSIBLE |
| Schoenberg PF∞ theory | Schoenberg 1947/1948 | PF∞ kernel | Variation-diminishing / real zeros | Unknown | Whether log-concavity implies PF∞ | OPEN |
| LP closure (Route B) | Standard | LP-class limits | LP class | Unknown | Construction of real-rooted approximants | OPEN |
| de Bruijn–Newman (Λ=0) | Rodgers–Tao 2018 | Λ = 0 | RH | TBD | Connection to log-concavity unknown | OPEN |
| $e^{-t^{2m}}$ class known result | Pólya 1926 (via Csordas-Varga) | $K(t) = e^{-t^{2m}}$ | Fourier has only real zeros | No (kernel, not $\Phi$) | Supports H13 on Class 2 kernels (COMPUTATION) | COMPUTATION |

---

## Summary of first iteration findings (2026-06-04)

**Sources acquired:** Cardon 2002 (full PDF), Csordas-Vishnyakova 2013 (full text),
Csordas-Varga 1989 (partial), Branden-Chasse 2014/2016 (arXiv).

**Status changes:**
- Pólya Hilfssatz II: POSSIBLE → **REJECT** (requires prior real-rootedness, exact statement confirmed)
- Cardon 2002: POSSIBLE → **REJECT** (all theorems require LP class input, no new bridge)
- "Csordas 2015": corrected to **Csordas-Vishnyakova 2013**, verdict **PARTIAL MATCH**
  (log-concavity = $L_1 \geq 0$ alone is insufficient; need all $L_n \geq 0$)
- Cardon 2005 (separate paper): newly identified as POSSIBLE — not yet acquired.

**Critical negative result confirmed:**
Log-concavity ($L_1 \geq 0$) alone does NOT imply real zeros for general entire functions.
Counterexample: $\phi = e^{x^2/2}\cos x$ (log-concave, but has non-real zeros, fails H5).
This shows H5 (superexponential decay) is a non-redundant hypothesis in H13.

**No bridge found. H13 remains OPEN.**

---

## Hard constraints for any valid bridge

A bridge theorem is valid for this project ONLY if it:

1. Has hypotheses that are all PROVED for Φ (not assumed).
2. Does NOT require prior real-rootedness of Ξ (circular).
3. Does NOT require Mellin condition unless Mellin condition is separately proved for Φ.
4. Is sourced from a primary publication (not secondary claim).
5. Has been verified against the primary text (not paraphrase only).
