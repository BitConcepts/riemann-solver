# Deliverable: proposition_8_expanded_ratio.md
# Proposition prop:tail_ratio — Expanded B_n Ratio Derivation

## Problem

Proposition `prop:tail_ratio` currently states without derivation:

```
|φ_n(u)|/φ₁(u) = B_n(u)·e^{-π(n²-1)e^{2u}} where B_n(u) = n²h_n(u)/h_1(u),
h_n = 2πn²e^{2u}-3.
Since B_n(u)/n⁴ ≤ 1+3/(2π-3) < 2 for all u ≥ 0 (see docs/tail_prefactor_correction.md)...
```

The bound B_n(u)/n⁴ < 2 is asserted with an external reference but not derived in-text.
For a proof-critical inequality (this controls the size of |R|/φ₁), the algebra should
be displayed.

---

## Complete Derivation

### Step 1: Definition of B_n

From the formula φ_n(u) = (2πn⁴e^{9u/2} - 3πn²e^{5u/2})·e^{-πn²e^{2u}}, the ratio is:

$$
\frac{|\varphi_n(u)|}{\varphi_1(u)}
= \frac{|2\pi n^4 e^{9u/2} - 3\pi n^2 e^{5u/2}|}{2\pi e^{9u/2} - 3\pi e^{5u/2}}
\cdot e^{-\pi(n^2-1)e^{2u}}
= B_n(u)\cdot e^{-\pi(n^2-1)e^{2u}},
$$

where:

$$
B_n(u) = \frac{n^2(2\pi n^2 e^{2u}-3)}{2\pi e^{2u}-3}
= \frac{2\pi n^4 e^{2u} - 3n^2}{2\pi e^{2u} - 3}.
$$

(The common factor π·e^{5u/2} cancels from numerator and denominator.)

### Step 2: Algebraic factoring

Add and subtract n⁴(2πe^{2u} - 3) in the numerator:

$$
2\pi n^4 e^{2u} - 3n^2
= n^4(2\pi e^{2u} - 3) + 3n^4 - 3n^2
= n^4(2\pi e^{2u} - 3) + 3n^2(n^2 - 1).
$$

Therefore:

$$
B_n(u)
= \frac{n^4(2\pi e^{2u}-3) + 3n^2(n^2-1)}{2\pi e^{2u}-3}
= n^4 + \frac{3n^2(n^2-1)}{2\pi e^{2u}-3}
= n^4 + \frac{3(n^4 - n^2)}{2\pi e^{2u}-3}.
$$

### Step 3: Bound on B_n(u)/n⁴

$$
\frac{B_n(u)}{n^4}
= 1 + \frac{3(1 - 1/n^2)}{2\pi e^{2u} - 3}.
$$

For all $n \geq 2$ and $u \geq 0$:
- $1 - 1/n^2 \leq 1$ (sharp at $n \to \infty$)
- $2\pi e^{2u} - 3 \geq 2\pi - 3 > 0$ for $u \geq 0$

Therefore:

$$
\frac{B_n(u)}{n^4}
\leq 1 + \frac{3}{2\pi - 3}
\approx 1 + \frac{3}{3.283}
\approx 1 + 0.9136
< 2.
$$

The bound is tight: at $n \to \infty$, $u = 0$, $B_n/n^4 \to 1 + 3/(2\pi - 3) \approx 1.914$.

### Step 4: Consequence

$$
\frac{|\varphi_n(u)|}{\varphi_1(u)} \leq 2n^4\,e^{-\pi(n^2-1)e^{2u}}.
$$

---

## Required Paper Text (LaTeX)

Replace the current terse statement:

```latex
Since $B_n(u)/n^4 \leq 1 + 3/(2\pi-3) < 2$ for all $u \geq 0$
(see \texttt{docs/tail\_prefactor\_correction.md})
```

With the following explicit derivation:

```latex
\textit{Derivation of $B_n/n^4 < 2$:}
$$
B_n(u)
= \frac{2\pi n^4 e^{2u} - 3n^2}{2\pi e^{2u} - 3}
= n^4 + \frac{3(n^4 - n^2)}{2\pi e^{2u} - 3},
$$
so
$$
\frac{B_n(u)}{n^4}
= 1 + \frac{3(1-1/n^2)}{2\pi e^{2u}-3}
\leq 1 + \frac{3}{2\pi - 3} < 2
$$
for all $n \geq 2$ and $u \geq 0$, using $1-1/n^2 \leq 1$ and $2\pi e^{2u} - 3 \geq 2\pi - 3 > 0$.
```

---

## Acceptance Criterion

The bound $B_n(u)/n^4 < 2$ must be derived in the paper body, not deferred to docs/.

**Status: RESOLVED** (algebraic derivation complete; requires paper text update).
