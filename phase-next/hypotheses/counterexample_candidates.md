# Counterexample Candidates for H13

**Purpose:** Try to disprove H13 before trying to prove it.

Falsification discipline: a counterexample candidate is only a disproof of H13 when ALL six
hypotheses are verified AND the Fourier transform is confirmed to have a complex zero by a
rigorous (argument-principle or interval-arithmetic) method.

---

## Hypothesis checklist

For any candidate kernel $K$, verify:

| Hypothesis | Symbol | Description |
|-----------|--------|-------------|
| H1 | even | $K(-t) = K(t)$ for all $t$ |
| H2 | positive | $K(t) > 0$ for all $t$ |
| H3 | integrable | $\int_{-\infty}^{\infty} K(t)\,dt < \infty$ |
| H4 | analytic | $K$ is real analytic near $t=0$ (and globally analytic) |
| H5 | superexp decay | $K(t) e^{c|t|} \to 0$ for all $c > 0$ as $|t|\to\infty$ |
| H6 | log-concave | $(\log K)''(t) \leq 0$ for all $t \geq 0$ |

---

## Candidate kernel classes

### Class 1 — Non-even power decay (control)

$K(t) = e^{-|t|^p}$, $p$ non-even integer.

- H4 fails: not analytic at $t=0$ for non-even $p$.
- Use as control: confirms falsification scripts reject non-analytic kernels.
- Expected Fourier behavior: known for $p=1$ (Cauchy), $p=2$ (Gaussian).

### Class 2 — Even power decay

$K(t) = e^{-t^{2m}}$, $m \geq 1$.

- All hypotheses H1–H6 satisfied for $m \geq 1$.
- $m=1$: Gaussian. Fourier transform is Gaussian — real zeros only (trivially, no zeros at all).
- $m \geq 2$: log-concavity fails for large $t$ ($(log K)'' = -2m(2m-1)t^{2m-2} < 0$ for $t>0$ only if $m=1$).
  - Actually: $(\log K)'' = -2m(2m-1)t^{2m-2}$. For $m=1$: $-2 < 0$. For $m=2$: $-12t^2 < 0$ for $t>0$. Log-concave for all $m \geq 1$.
  - Fourier transform of $e^{-t^4}$: known to have only real zeros? **CHECK in experiments.**
- Status: CANDIDATE — needs Fourier zero computation.

### Class 3 — Gaussian perturbations

$K(t) = e^{-t^2 - \varepsilon t^4 + \text{small analytic perturbations}}$, $\varepsilon > 0$.

- Close to Gaussian. Log-concavity: $(\log K)'' = -2 - 12\varepsilon t^2 < 0$.
- All hypotheses satisfied for small $\varepsilon$.
- Fourier zeros: expect real-only near Gaussian. Useful near-counterexample probe.

### Class 4 — Compactly modified analytic log-concave kernels

Bump-function modifications of Gaussian that preserve all hypotheses.
Expected to be hard to construct without violating analyticity.

### Class 5 — Mixture kernels

$K(t) = \lambda K_1(t) + (1-\lambda) K_2(t)$.
Mixtures preserve positivity and integrability but may not preserve log-concavity.
Use to generate test cases where log-concavity is marginal.

### Class 6 — One-hypothesis-at-a-time violations

Test necessity of each hypothesis by dropping it:
- Drop H4 (analyticity): does non-analytic log-concave kernel ever have complex Fourier zeros?
- Drop H5 (superexp decay): slower decay, log-concave — does Fourier develop complex zeros?
- Drop H6 (log-concavity): analytic, positive, even, integrable, decaying but NOT log-concave — complex Fourier zeros?

---

## Candidate log

| Kernel | Hypotheses satisfied | Fourier zero test | Status |
|--------|---------------------|-------------------|--------|
| $e^{-t^2}$ | H1-H6 all | No zeros | TRIVIAL (no zeros) |
| $e^{-t^4}$ | H1-H6 check needed | TBD | CANDIDATE |
| $e^{-t^2 - 0.1t^4}$ | H1-H6 likely | TBD | CANDIDATE |
| $e^{-\|t\|^{1.5}}$ | H4 fails | TBD | CONTROL |

---

## Decision protocol

1. Generate candidate kernel.
2. Verify all six hypotheses numerically (and analytically where possible).
3. Compute Fourier transform numerically (high precision).
4. Use argument principle to count zeros in boxes $\{|z| < R, |\text{Im}(z)| > \delta\}$.
5. If complex zero found: classify which hypotheses hold, escalate to rigorous verification.
6. If no complex zero found up to $R$: record as "no counterexample found in box."
7. Never report as disproof without rigorous verification of all hypotheses.
