# Modern Real-Zero Criteria for Fourier Transforms

Survey of post-1989 literature on conditions for Fourier transforms to have only real zeros.
Updated each iteration.

---

## Cardon 2002

**Citation:** D.A. Cardon, "Convolution operators and zeros of entire functions,"
Proc. Amer. Math. Soc. 130 (2002), no. 6, 1725–1734.
DOI: https://doi.org/10.1090/S0002-9939-01-06351-1

**Status:** ACQUIRED — Iteration 1. REJECT as bridge.

**Key result:** All theorems require G ∈ LP* (already has only real zeros).
Hilfssatz II quoted: requires prior real-rootedness. Circular for Ξ.

---

## Cardon 2005

**Citation:** D.A. Cardon, "Fourier transforms having only real zeros,"
Proc. Amer. Math. Soc. 133 (2005), no. 5, 1349–1356.
DOI: https://doi.org/10.1090/s0002-9939-04-07677-4

**Status:** ACQUIRED — Iteration 2a. REJECT as bridge.

**Key result (Theorem 1):** Given G ∈ LP* (real entire, order < 2, only real zeros)
and a distribution F from normalized sums of ±1 random variables,
H(z) = ∫G(it)e^{izt}dF(t) has only real zeros.

**Assessment:** PRESERVATION theorem. Requires G to already have only real zeros.
Does NOT use log-concavity. Does NOT provide a bridge from kernel properties
to real zeros of Fourier transform. Applying to RH would require Ξ already real-rooted.

---

## Cardon 2009

**Citation:** D.A. Cardon, "Extended Laguerre inequalities and a criterion for real zeros,"
Progress in Analysis and its Applications (2010), pp. 143–149.

**Status:** Content reconstructed from citations. PARTIAL MATCH.

**Key result:** Extends the generalized Laguerre operator framework. Csordas-Vishnyakova 2013
call this an "ingenious extension of the Laguerre-type inequalities." However, the
fundamental criterion remains: ALL L_n ≥ 0 for all n ≥ 0 is needed, not just L_1 ≥ 0.
Cardon's extension does not bridge the gap between L_1 (log-concavity) and all L_n.

**Open conjecture:** Csordas-Vishnyakova 2013 Conjecture 3.3 (based on Cardon's work):
under suitable conditions, L_1 ≥ 0 might imply all L_n ≥ 0. UNPROVED.

---

## Brandén–Chasse 2016

**Citation:** P. Brandén, M. Chasse, "Classification theorems for operators preserving
zeros in a strip," J. Anal. Math. (2017). arXiv:1402.2795.

**Status:** ACQUIRED — Iteration 2a.

**Key results:**
- **Theorems 1.1, 1.2:** Complete characterization of strip-preserving operators for
  complex polynomials. Solves Problem 1 for closed strips.
- **Theorems 4.5, 4.7:** Sharp sufficient conditions for differential operators to
  contract zeros toward real axis (property (I) of strong universal factors).
- **Section 5:** Extends de Bruijn–Ilieff theorem. Sufficient condition for Fourier
  transform to have only real zeros: K(t) = exp(-h(t)) where h'(t) ∈ LP
  (derivative is uniform limit of polynomials with purely imaginary zeros).

**Assessment for H13:** The de Bruijn–Ilieff route requires h'(t) ∈ LP for
h(t) = -log Φ(t). This is a DIFFERENT condition from log-concavity of Φ.
Log-concavity = (Φ')^2 - ΦΦ'' ≥ 0, while h' ∈ LP requires all zeros of h'
to be purely imaginary. The bridge between these conditions is unknown.

**Verdict:** LP CONDITION ON DERIVATIVE — not directly applicable as bridge.
However, the de Bruijn–Ilieff route (Route C) is a promising avenue:
if h'(t) = -(Φ'/Φ)(t) can be shown to have only imaginary zeros, then
the theorem would apply. This is a new route not previously identified.

---

## Coffey–Csordas 2013

**Citation:** TBD

**Status:** Not yet acquired.

**Relevance:** Cited in phase-next prompt as relevant; may concern generalized Laguerre
inequalities or RH-related functional inequalities.

---

## Rodgers–Tao 2018 — Proof that Λ ≥ 0

**Citation:** B. Rodgers, T. Tao, "The de Bruijn–Newman constant is non-negative,"
Forum Math. Pi 8 (2020), e6.
DOI: https://doi.org/10.1017/fmp.2020.6

**Status:** Published. Establishes RH ⟺ Λ = 0.

**Relation to H13:** Does not use log-concavity. Separate approach via heat flow.

---

## Schoenberg — Pólya frequency functions / total positivity

**Key works:**
- I.J. Schoenberg, "On totally positive functions, Laplace integrals and entire functions of
  the Laguerre–Pólya–Schur type," Proc. Natl. Acad. Sci. USA 33 (1947), 11–17.
- I.J. Schoenberg, "On variation-diminishing integral operators of the convolution type,"
  Proc. Natl. Acad. Sci. USA 34 (1948), 164–169.

**Key question for Route A:** Does PF∞ (total positivity) of a kernel imply real-rooted
Fourier transform? If yes, does log-concavity + analyticity + decay imply PF∞?

**Status:** Not yet extracted — Route A investigation.

---

## Notes on the general state of H13

As of the first iteration, NO known theorem in the literature is confirmed to have:
- Hypotheses: positivity + evenness + integrability + real analyticity + superexponential decay + log-concavity on [0,∞)
- Conclusion: Fourier transform has only real zeros
- No circular prior-real-rootedness assumption
- No Mellin condition
- No LP-class membership of derivative

H13 appears to be genuinely open or equivalent to a known open problem. This assessment
will be updated as sources are inspected.
