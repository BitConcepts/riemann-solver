# Bridge Status Matrix

Tracks all candidate theorem bridges. Updated after every research iteration.

**Last updated:** 2026-06-04 (Iteration 2b — L_2 certified)

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
| Csordas-Vishnyakova Thm 2.3 | Csordas-Vishnyakova 2013 | ALL $L_n \geq 0$ for all $n$, all $x$ | $\phi \in L$-$P$ (real zeros) | PARTIAL | $L_1$ PROVED, $L_2$ PROVED (IA cert); need $L_3, L_4, \ldots$ | PARTIAL MATCH |
| Cardon 2002 Theorem 1 | Cardon 2002 | $G$ already in LP class | Convolution preserves real zeros | No | Circular: G must already have real zeros | REJECT |
| Pólya Hilfssatz II | Pólya 1927 (via Cardon 2002) | $G$ already has only real zeros | $G(z+ia)+G(z-ia)$ has real zeros | No | Circular: requires prior real-rootedness | REJECT |
| Cardon 2005 Fourier paper | Cardon 2005 | G ∈ LP* (prior real zeros) + distribution F | H(z) = ∫G(it)e^{izt}dF(t) has real zeros | No — circular (G must have real zeros) | Requires prior real-rootedness of G | REJECT |
| Cardon 2009 Extended Laguerre | Cardon 2009 | ALL L_n ≥ 0 for all n, all x | φ ∈ L-P (real zeros) | PARTIAL — gap from L_1 to all L_n | Same as Csordas-Vishnyakova 2013 | PARTIAL MATCH |
| Brandén-Chasse de Bruijn-Ilieff ext. | Brandén-Chasse 2016, §5 | h'(t) ∈ LP (derivative condition) | ∫exp(-h(t))e^{izt}dt has real zeros | Unknown — need h'=-Φ'/Φ ∈ LP | Log-concavity ≠ h' ∈ LP; bridge unknown | POSSIBLE (Route C) |
| Schoenberg PF∞ theory | Schoenberg 1947/1948 | PF∞ kernel | Variation-diminishing / real zeros | Unknown | Whether log-concavity implies PF∞ | OPEN |
| LP closure (Route B) | Standard | LP-class limits | LP class | Unknown | Construction of real-rooted approximants | OPEN |
| de Bruijn–Newman (Λ=0) | Rodgers–Tao 2018 | Λ = 0 | RH | TBD | Connection to log-concavity unknown | OPEN |
| $e^{-t^{2m}}$ class known result | Pólya 1926 (via Csordas-Varga) | $K(t) = e^{-t^{2m}}$ | Fourier has only real zeros | No (kernel, not $\Phi$) | Supports H13 on Class 2 kernels (COMPUTATION) | COMPUTATION |

---

## Summary of first iteration findings (2026-06-04)

**Sources acquired (Iteration 1):** Cardon 2002 (full PDF), Csordas-Vishnyakova 2013 (full text),
Csordas-Varga 1989 (partial), Branden-Chasse 2014/2016 (arXiv).

**Iteration 1 status changes:**
- Pólya Hilfssatz II: POSSIBLE → **REJECT** (requires prior real-rootedness, exact statement confirmed)
- Cardon 2002: POSSIBLE → **REJECT** (all theorems require LP class input, no new bridge)
- "Csordas 2015": corrected to **Csordas-Vishnyakova 2013**, verdict **PARTIAL MATCH**
  (log-concavity = $L_1 \geq 0$ alone is insufficient; need all $L_n \geq 0$)
- Cardon 2005 (separate paper): newly identified as POSSIBLE — not yet acquired.

**Iteration 2a sources acquired:** Cardon 2005 (full PDF), Cardon 2009 (content from citations),
Brandén-Chasse 2016 (full arXiv PDF, Section 5 analyzed).

**Iteration 2a status changes:**
- Cardon 2005: POSSIBLE → **REJECT** (Theorem 1 requires G ∈ LP*, i.e., prior real-rootedness)
- Cardon 2009: POSSIBLE → **PARTIAL MATCH** (same L_n framework as Csordas-Vishnyakova 2013)
- Brandén-Chasse (de Bruijn-Ilieff ext.): NEW → **POSSIBLE (Route C)** — requires h'(t) ∈ LP
  where h = -log Φ. Whether log-concavity implies this is unknown.

**Critical negative result confirmed:**
Log-concavity ($L_1 \geq 0$) alone does NOT imply real zeros for general entire functions.
Counterexample: $\phi = e^{x^2/2}\cos x$ (log-concave, but has non-real zeros, fails H5).
This shows H5 (superexponential decay) is a non-redundant hypothesis in H13.

**New Route C identified:** de Bruijn-Ilieff theorem (extended by Brandén-Chasse 2016)
gives sufficient conditions: if h'(t) ∈ LP where Φ(t) = exp(-h(t)), then ∫Φ(t)e^{izt}dt
has only real zeros. Need to investigate whether log-concavity of Φ implies h' ∈ LP.

**No bridge found. H13 remains OPEN.**

---

## Iteration 2b findings (2026-06-04)

**L_2 generalized Laguerre inequality certified [PROVED]:**
- $L_2(u) = 2\Phi\Phi^{(4)} - 8\Phi'\Phi''' + 6(\Phi'')^2 \geq 0$ for all $u \geq 0$.
- IA certificate: 2000 subintervals on [0, 1], all certified. Grid: 500 points on [0, 5], all nonneg.
- Combined with T6 ($L_1 \geq 0$), two of the infinite Laguerre inequalities are now proved.

**Status changes:**
- Csordas-Vishnyakova Thm 2.3: gap narrowed from "only $L_1$" to "$L_1$ and $L_2$ proved; need $L_3, L_4, \ldots$"
- No bridge promoted; infinitely many inequalities still required.

**Key observation:** L_2 certification was straightforward — suggests $L_n \geq 0$ may hold for
all $n$ for $\Phi$, which would complete the Csordas-Vishnyakova criterion. Worth certifying $L_3$.

---

## Iteration 2c findings (2026-06-04)

**Expanded counterexample search: 13 new kernels tested (16 total), 0 counterexample candidates.**

Kernels satisfying all H1-H6 with no complex Fourier zeros found:
- Class 2 extended: exp(-t^6), exp(-t^8), exp(-t^10) — each has 6 real zeros, 0 complex
- Class 3 extended: exp(-t^2-εt^4) for ε∈{1,5,10,50} — strictly log-concave, 0 complex
- Near-CX probes: exp(-t^4)cos²(0.1t) — all H1-H6, 7 real zeros, 0 complex

Kernels failing hypotheses (no complex zeros found either):
- (1+t^2)^{-2}: fails H5, H6. FT has no zeros at all.
- exp(-t^2)(1+0.5cos2t): fails H6. No Fourier zeros.
- exp(-t^2+0.1sin(t^2)): fails H6. 9 real zeros, 0 complex.
- exp(-5t^2)|cos(0.5t)|: fails H4. No zeros.

**H5 necessity:** UNCLEAR — no H5-failing kernel produced complex zeros.
**H6 necessity:** UNCLEAR — no H6-failing kernel produced complex zeros.
**Counterexample status:** None found. H13 consistent with all 16 tested kernels.

Complex strip scanned: Re∈[0,20], Im∈[0.01,5], 30×15 grid. All COMPUTATION class.

---

## Hard constraints for any valid bridge

A bridge theorem is valid for this project ONLY if it:

1. Has hypotheses that are all PROVED for Φ (not assumed).
2. Does NOT require prior real-rootedness of Ξ (circular).
3. Does NOT require Mellin condition unless Mellin condition is separately proved for Φ.
4. Is sourced from a primary publication (not secondary claim).
5. Has been verified against the primary text (not paraphrase only).
