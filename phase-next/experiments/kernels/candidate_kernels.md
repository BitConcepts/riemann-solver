# Candidate Kernels for H13 Counterexample Search

Each kernel class is evaluated against the six H13 hypotheses.
Results updated as experiments run.

---

## Class 1 — Non-even power decay (control)

**Kernel:** $K(t) = e^{-|t|^p}$, $p \notin 2\mathbb{Z}_{>0}$

**Purpose:** Control class to verify that falsification scripts correctly reject kernels
that fail analyticity.

**Hypothesis check:**
- H1 (even): ✓
- H2 (positive): ✓
- H3 (integrable): ✓
- H4 (analytic): ✗ — not analytic at $t=0$ for non-integer or odd-integer $p$
- H5 (superexp decay): ✓ for $p > 0$
- H6 (log-concave): $(\log K)'' = -p(p-1)|t|^{p-2}$. For $p>1$: negative for $t>0$. ✓

**Expected outcome:** Scripts classify as `invalid candidate` due to H4 failure.

---

## Class 2 — Even power decay

**Kernel:** $K(t) = e^{-t^{2m}}$, $m = 1, 2, 3, 4$

**Purpose:** Simplest analytic, even, positive, integrable, log-concave kernels satisfying all hypotheses.

**Hypothesis check (for all $m \geq 1$):**
- H1 (even): ✓
- H2 (positive): ✓
- H3 (integrable): ✓ ($\Gamma(1+1/(2m)) / m$ finite)
- H4 (analytic): ✓ (entire function)
- H5 (superexp decay): ✓ (faster than any exponential)
- H6 (log-concave): $(\log K)'' = -2m(2m-1)t^{2m-2}$
  - $m=1$: $= -2 < 0$ ✓
  - $m=2$: $= -12t^2 \leq 0$ (equals 0 at $t=0$) — marginal log-concavity
  - $m \geq 2$: $\leq 0$, equals 0 at $t=0$ ✓ (weakly log-concave)

**Note on $m=1$:** Gaussian. Fourier transform is Gaussian (no zeros). Trivial case.

**Key experiment:** For $m=2,3,4$: Does $\hat{K}(\xi) = \int e^{-t^{2m}} e^{i\xi t} dt$
have only real zeros? Literature suggests yes for $m=2$ but rigorous verification needed.

**Status:** CANDIDATE — run in search_counterexamples.py.

---

## Class 3 — Gaussian perturbations

**Kernel:** $K_\varepsilon(t) = e^{-t^2 - \varepsilon t^4}$, $\varepsilon > 0$

**Purpose:** Deform from Gaussian toward Class 2 ($m=2$) while monitoring zero positions.

**Hypothesis check:**
- H1–H3: ✓
- H4: ✓ (entire)
- H5: ✓
- H6: $(\log K_\varepsilon)'' = -2 - 12\varepsilon t^2 < 0$ ✓ (strictly log-concave)

**Experiments:** $\varepsilon \in \{0.01, 0.1, 0.5, 1.0, 5.0, 10.0\}$

---

## Class 4 — Gaussian + cosine perturbation

**Kernel:** $K(t) = e^{-t^2}(1 + a\cos(\omega t))$ for small $a$

**Purpose:** Test whether small oscillation in kernel can induce complex Fourier zeros,
while checking whether log-concavity is preserved.

**Warning:** Log-concavity may fail for large $a$ or $\omega$. Must check H6 numerically.

**Status:** CANDIDATE — check H6 before Fourier zero search.

---

## Class 5 — Two-component mixture

**Kernel:** $K(t) = \lambda e^{-t^2} + (1-\lambda) e^{-t^4}$, $\lambda \in (0,1)$

**Purpose:** Mixtures of Class 2 kernels. Log-concavity of mixture not guaranteed — must check.

**Note:** Sum of log-concave functions is NOT generally log-concave. This class may fail H6.

---

## Class 6 — One-hypothesis-at-a-time violations

### 6a — Drop H4 (analyticity)

$K(t) = e^{-|t|^3}$ — log-concave (for $t>0$: $(\log K)'' = -6|t| \leq 0$), positive, even,
integrable, fast decay, but NOT analytic at 0.

**Expected:** Script marks H4 = False. Even so: does Fourier transform have complex zeros?

### 6b — Drop H5 (superexponential decay)

$K(t) = e^{-t^2}/(1+t^2)$ — modifies decay rate. Verify whether log-concavity holds.

### 6c — Drop H6 (log-concavity)

$K(t) = e^{-t^2 + \sin(t^2)}$ — potentially non-log-concave.

**Purpose:** If complex Fourier zeros are found when H6 is dropped, confirms log-concavity
plays a necessary role.

---

## Results log

| Kernel | m / ε / params | All H1-H6? | Complex zeros found | Status |
|--------|----------------|-----------|---------------------|--------|
| $e^{-t^2}$ | m=1 | ✓ | No (Gaussian, trivial) | INVALID (trivial) |
| $e^{-t^4}$ | m=2 | Check H6 at 0 | TBD | CANDIDATE |
| $e^{-t^6}$ | m=3 | Check H6 at 0 | TBD | CANDIDATE |
| $e^{-t^2-0.1t^4}$ | ε=0.1 | ✓ | TBD | CANDIDATE |
| $e^{-\|t\|^3}$ | — | H4 fails | TBD | CONTROL |
