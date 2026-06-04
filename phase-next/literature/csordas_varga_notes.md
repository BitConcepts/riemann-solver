# Csordas–Varga 1989 and Csordas 2015 Notes

---

## Csordas–Varga 1989

**Citation:** G. Csordas, R.S. Varga, "Necessary and sufficient conditions and the Riemann
Hypothesis," Adv. Appl. Math. 11 (1989), 328–357.
DOI: https://doi.org/10.1016/0196-8858(89)90026-0

### Theorem 2.2 (paraphrase from secondary sources)

Restates Pólya Satz II in modern notation. Let $K(x) = \int_0^\infty \Phi(t) \cos(xt)\,dt$.
RH is equivalent to $K$ having only real zeros. Connects to the Mellin condition on $\Phi$.

**Verdict:** MELLIN CONDITION ONLY. Does not directly use log-concavity.

---

## Csordas & Vishnyakova 2013 — IDENTIFIED AND EXTRACTED

**Correct citation:** G. Csordas, A. Vishnyakova, "The generalized Laguerre inequalities and
functions in the Laguerre-Pólya class," *Open Mathematics* (formerly Central European Journal
of Mathematics) 11(9), 1643–1650 (2013).
DOI: https://doi.org/10.2478/s11533-013-0269-x
Full text: https://www.degruyterbrill.com/document/doi/10.2478/s11533-013-0269-x/pdf

**Note:** The prompt references "Csordas 2015 Theorems 3.5-3.7". The only Csordas paper
matching the described content is this 2013 paper. Theorem numbering and year may have been
misremembered. The theorems below are the actual results from the 2013 paper.

---

### Generalized Laguerre operators (Definition)

For a real entire function $\phi(x)$ and $n \in \mathbb{N}_0$, define:
$$L_n(x) = \sum_{j=0}^{2n} (-1)^{j+n} \frac{(2n)!}{j!(2n-j)!} \phi^{(j)}(x)\phi^{(2n-j)}(x)$$

**Key identity (equation (1) in paper):**
$$|\phi(x+iy)|^2 = \phi(x+iy)\phi(x-iy) = \sum_{n=0}^{\infty} L_n(x) y^{2n}$$

Special cases:
- $L_0(x) = \phi(x)^2 \geq 0$: trivially satisfied.
- $L_1(x) = (\phi'(x))^2 - \phi(x)\phi''(x) \geq 0$: this is the **standard Laguerre inequality**,
  equivalent to **log-concavity** of $\phi$. The current paper certifies $L_1 \geq 0$ for $\Phi$.

---

### Theorem 1.2 (from Csordas-Varga 1990, cited in paper) — necessary condition

**Statement:** If $\phi(x) \in L$-$P$, then $L_n(x) \geq 0$ for all $n \in \mathbb{N}_0$ and
for all $x \in \mathbb{R}$.

**Verdict:** NECESSARY ONLY. Log-concavity ($L_1 \geq 0$) is necessary for LP membership,
but not sufficient by itself.

**Counterexample showing $L_1 \geq 0$ is insufficient:** The paper explicitly gives
$\phi(x) = e^{x^2/2}\cos x$, which satisfies $L_1(x) = e^{x^2}\sin^2 x \geq 0$ for all
$x \in \mathbb{R}$, but $\phi \notin L$-$P$ (it has non-real zeros $x = \pi/2 + n\pi + iy$
for $y \neq 0$).

**CRITICAL FOR H13:** This counterexample directly shows that log-concavity alone
($L_1 \geq 0$, equivalently $(\log\phi)'' \leq 0$) does NOT imply real zeros for a general
entire function. H13 may still hold for the specific Riemann-Jacobi kernel $\Phi$ due to
its additional special properties (superexponential decay, specific analytic structure),
but it is NOT a consequence of log-concavity alone for general entire functions.

---

### Theorem 2.3 (Main theorem of Csordas-Vishnyakova 2013) — sufficient condition

**Statement:** Let $\phi(x)$ be a real entire function, $\phi \not\equiv 0$. If
$L_n(x) \geq 0$ for ALL $n \in \mathbb{N}_0$ and for ALL $x \in \mathbb{R}$, then:
(i) $\phi(x)$ has only real zeros; and (ii) $\phi(x) = e^{-ax^2}\phi_1(x)$, $a \geq 0$,
where $\phi_1(x)$ has genus 0 or 1. In particular, $\phi(x) \in L$-$P$.

**Hypotheses:** ALL generalized Laguerre inequalities $L_n \geq 0$ hold for all $n$ and all $x$.

**Verdict for H13:** PARTIAL MATCH. Theorem 2.3 gives a criterion for real-rootedness,
but requires ALL orders, not just $L_1$ (log-concavity). The current proof establishes
only $L_1 \geq 0$ for $\Phi$. Higher orders $L_2, L_3, \ldots$ are NOT verified.

**Gap for H13/Φ:** Need $L_n(x) \geq 0$ for ALL $n \geq 0$ and all $x \in \mathbb{R}$ for $\Phi$.
Log-concavity gives only $L_1 \geq 0$.

---

### Key negative result — Cardon-related conjecture

The paper (Section 3) mentions a conjecture (based on Cardon's work) that if $L_1 \geq 0$
(log-concavity) under suitable conditions, the higher $L_n \geq 0$ might follow. This is
stated as an **OPEN CONJECTURE**, not a proved theorem.

---

### Csordas-Dimitrov-Varga "Conjectures and Theorems" paper (related, ~2000)

**Citation:** G. Csordas, D.K. Dimitrov, "Conjectures and theorems in the theory of entire
functions," *Numerical Algorithms* 25 (2000), 109–122.

From the full text (retrieved):
"today, there are no known explicit necessary and sufficient conditions which a function
must satisfy in order that its Fourier transform have only real zeros."

This statement from the Csordas-Varga 1989 paper is still essentially true. H13 remains
open as of all retrieved sources.

---

### Pólya's result on $F(z; p) = \int_0^\infty e^{-t^p} \cos(zt) dt$ (from Csordas-Varga 1989)

**Critical finding for counterexample search (Csordas-Varga, Example 2.1):**
- For $p = 4, 6, 8, \ldots$ (even integers $\geq 4$): $F(z; p)$ has ONLY REAL ZEROS.
- For $p$ NOT an even integer: $F(z; p)$ has INFINITELY MANY NON-REAL ZEROS.

**Implication:** Kernels $e^{-t^p}$ with non-even-integer $p$ fail H4 (not analytic at $t=0$).
Among H4-satisfying kernels $e^{-t^{2m}}$, all have only real Fourier zeros (consistent
with H13). This is COMPUTATION-class supporting evidence for H13 on Class 2 kernels.

---

## Follow-up

- [x] Identify Csordas paper from prompt (resolved: Csordas-Vishnyakova 2013).
- [x] Extract main theorem (Theorem 2.3) verbatim.
- [x] Determine that log-concavity = $L_1 \geq 0$ is only NECESSARY, not sufficient.
- [ ] Investigate whether higher $L_n \geq 0$ for $\Phi$ can be computationally certified.
- [ ] Follow up on Cardon 2009 "Extended Laguerre inequalities and a criterion for real zeros."
- [ ] Check whether the counterexample $\phi = e^{x^2/2}\cos x$ satisfies H5 (superexp decay);
  if not, H5 may be the distinguishing condition between H13 and Csordas Thm 2.3.
