# Research Log — Phase-next

Chronological record of all research iterations. Each entry records what was done,
what was found, and what the next action is.

---

## Iteration 0 — Setup (2026-06-04)

**Objective:** Establish branch structure and populate baseline files.

**Actions taken:**
- Created `phase-next/` directory structure.
- Populated H13_statement.md with full problem statement and evidence table.
- Populated bridge_status_matrix.md with 13 candidate theorems.
- Populated source_index.md with 5 initial sources.
- Created skeleton files for all literature, experiments, formal, and reports directories.

**Claim status:**
```
PROVED:      Certified strict log-concavity of Φ on [0, ∞).
OPEN:        H13 — log-concavity-to-real-rootedness bridge.
CONDITIONAL: RH under H13.
```

**Iteration verdict:**
- Route: Setup only
- New evidence: None — structure only
- Advances path 1/2/3: No
- Remaining gap: H13 entirely open
- Next action: Iteration 1 — Cardon 2002 literature scan + counterexample search

---

## Iteration 1 — Cardon 2002 / Hilfssatz II + Csordas 2013 (2026-06-04)

**Status:** COMPLETE

**Sources acquired:**
1. Cardon 2002 (full PDF retrieved from AMS): "Convolution operators and zeros of entire functions,"
   Proc. Amer. Math. Soc. 130 (2002), 1725–1734.
2. Csordas-Vishnyakova 2013 (full text retrieved): "The generalized Laguerre inequalities and
   functions in the Laguerre-Pólya class," Open Mathematics 11(9), 1643–1650.
3. Csordas-Varga 1989 (partial, from CORE): "Necessary and sufficient conditions and the
   Riemann Hypothesis," Adv. Appl. Math. 11 (1990), 328–357.
4. Branden-Chasse 2014/2016 (arXiv:1402.2795): strip preservers and Fourier real zeros.

**Key findings:**

### Finding 1: Pólya Hilfssatz II — REJECT

Exact statement (from Cardon 2002, p. 1726):
> Let $a$ be a positive constant and let $G(z)$ be an entire function of genus 0 or 1 that
> for real $z$ takes real values, has at least one real zero, and has only real zeros.
> Then the function $G(z+ia)+G(z-ia)$ has only real zeros.

Verdict: PRESERVATION ONLY. Requires $G$ to already have only real zeros.
Applying to $\Phi$ would require $\Xi$ to already have only real zeros — circular.
Status change: POSSIBLE → REJECT.

### Finding 2: Csordas-Vishnyakova 2013 ("Csordas 2015" in prompt) — PARTIAL MATCH

The prompt's "Csordas 2015 Theorems 3.5–3.7" refers to Csordas-Vishnyakova (2013).
Theorem numbering differs; the key result is Theorem 2.3:

> If $L_n(x) \geq 0$ for ALL $n \geq 0$ and ALL $x \in \mathbb{R}$, then $\phi \in L$-$P$.

- $L_1 = (\phi')^2 - \phi\phi'' \geq 0$ is log-concavity. Current paper proves this for $\Phi$.
- But Theorem 2.3 requires ALL $L_n \geq 0$, not just $L_1$.
- There exists a counterexample: $\phi = e^{x^2/2}\cos x$ satisfies $L_1 \geq 0$ (log-concave)
  but has non-real zeros. PROVES log-concavity alone is insufficient for general entire functions.
- An open conjecture in the paper suggests $L_1 \geq 0$ might imply all $L_n \geq 0$ under
  suitable conditions — but this is unproved.

Status change: POSSIBLE → PARTIAL MATCH with identified gap.

### Finding 3: Known negative result on H13 for general entire functions

From Csordas-Varga 1989: "today, there are no known explicit necessary and sufficient
conditions which a function must satisfy in order that its Fourier transform have only real
zeros." (Still essentially true.)

From Csordas-Varga 1989, Example 2.1 (Pólya's result):
- $\int_0^\infty e^{-t^p}\cos(zt)dt$ has ONLY REAL zeros for $p \in \{4, 6, 8, \ldots\}$.
- But has INFINITELY MANY NON-REAL zeros for $p$ not an even integer.
- Non-even $p$ kernels fail H4 (analyticity at 0). So Class 2 kernels ($p = 2m$) are consistent
  with H13 holding (COMPUTATION class support).

### Finding 4: Counterexample to H13 in general (not for Φ)

The function $\phi(x) = e^{x^2/2}\cos x$ is log-concave ($L_1 \geq 0$) but has non-real zeros.
However, this is NOT a counterexample to H13 for $\Phi$ because:
- $e^{x^2/2}\cos x$ fails H5 (superexponential decay): it GROWS, not decays.
- H5 (superexponential decay) is a genuine hypothesis distinguishing $\Phi$ from this example.
- This shows H5 is DOING REAL WORK in H13. It is NOT redundant.

### Finding 5: Cardon 2005 paper identified but not yet acquired

Cardon (2005): "Fourier transforms having only real zeros," Proc. Amer. Math. Soc. 133 (2005),
1349–1356. DOI: 10.1090/s0002-9939-04-07677-4. Full PDF available at Cardon's BYU webpage.
This paper may have results more directly relevant than Cardon 2002. Targeted for Iteration 2.

**Iteration verdict:**
- Route advanced: NONE — no bridge found
- Advances path 1: No
- Advances path 2: No — Hilfssatz II REJECTED; Csordas 2013 requires more than log-concavity
- Advances path 3: Partial — identified that log-concavity alone is insufficient for general
  entire functions; H5 (superexp decay) is non-redundant
- Remaining gap: Need ALL $L_n \geq 0$ for $\Phi$, not just $L_1$; OR need a new approach
- Next action: (1) Acquire Cardon 2005; (2) Computationally certify $L_2 \geq 0$ for $\Phi$
  (second Laguerre inequality); (3) Run counterexample search experiments.

---

---
