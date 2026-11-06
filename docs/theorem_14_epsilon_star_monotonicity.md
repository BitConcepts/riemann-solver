# Deliverable: theorem_14_epsilon_star_monotonicity.md
# Theorem thm:perturbation_tail — Fix ε* Monotonicity Statement

## Problem

The proof of Theorem `thm:perturbation_tail` (Tail Bound for u ≥ 3) contains:

```
ε is strictly decreasing. Each term satisfies
d/du[n⁴ e^{-π(n²-1)e^{2u}}] = -2π(n²-1)e^{2u}·n⁴e^{-π(n²-1)e^{2u}} < 0
for all n≥2 and u≥0.
```

The proof uses ε* throughout (correct), but then says "ε is strictly decreasing" (old
notation). This is a notation inconsistency: the function being differentiated and shown
negative is ε*, not ε_old.

---

## Required Fix

### In the paper text

Locate the line:

```latex
\emph{$\varepsilon$ is strictly decreasing.} Each term satisfies
$\tfrac{d}{du}\bigl[n^4 e^{-\pi(n^2-1)e^{2u}}\bigr] = -2\pi(n^2-1)e^{2u}\cdot n^4
e^{-\pi(n^2-1)e^{2u}} < 0$
for all $n\geq 2$ and $u\geq 0$.
```

Replace with:

```latex
\emph{$\varepsilon_*$ is strictly decreasing}, since it is twice a sum of strictly
decreasing positive terms. For each $n\geq 2$ and $u\geq 0$:
$$
\frac{d}{du}\bigl[2n^4 e^{-\pi(n^2-1)e^{2u}}\bigr]
= -4\pi(n^2-1)e^{2u}\cdot n^4\,e^{-\pi(n^2-1)e^{2u}} < 0.
$$
Summing over $n\geq 2$ (justified by dominated convergence), $\varepsilon_*'(u)<0$.
```

---

## Why This Matters

1. **Notation consistency**: The proof defines ε*(u) = 2·Σ n⁴ e^{-π(n²-1)e^{2u}} but
   then says "ε is decreasing" — a reviewer will flag this.

2. **Factor of 2**: The derivative of the individual ε* term includes the factor of 2,
   giving -4π(n²-1)e^{2u}·n⁴e^{-π(n²-1)e^{2u}}, not -2π(n²-1)e^{2u}·n⁴e^{-...}.
   The current text shows the derivative of an ε_old term, not an ε* term.

3. **Clarity**: "twice a sum of strictly decreasing positive terms" makes the argument
   explicit and unambiguous.

---

## Consistency with Sublemma 12.1

Note that Sublemma 12.1 Part (a) (from lemma_12_hardening.md) also proves
ε*'(u) < 0 with the explicit bound d/du log ε* ≤ -6πe^{2u}. The proof of
Theorem thm:perturbation_tail can reference this:

```latex
\emph{$\varepsilon_*$ is strictly decreasing} by Sublemma~\ref{sublem:lambda_decay}(a);
in particular $\varepsilon_*'(u) < 0$ for all $u \geq 0$.
```

This avoids repeating the derivative computation.

---

## Acceptance Criterion

After fix: the proof of thm:perturbation_tail uses only ε* (not ε or ε_old), and the
derivative shown matches the definition of ε* including the factor of 2.

**Status: FIXED** (notation-only correction plus factor-of-2 in derivative).
