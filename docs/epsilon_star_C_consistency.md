# Deliverable: epsilon_star_C_consistency.md
# ε* Notation and C=204 Consistency in Theorem thm:extended

## Problem

Theorem `thm:extended` (Extended Certification on [1,3]) currently defines:

```
C := |ΔQ| / (ε · |Q_{φ₁}|)|_{u=1} = 204,
    ε(1) = 9.59×10⁻³⁰,    |ΔQ|/|Q_{φ₁}| = 1.95×10⁻²⁷.
```

But the theorem applies the bound as `|W_tail| ≤ C·ε*(u)` where `ε*(u) = 2ε_old(u)`.
This mixes the definition of C (computed with ε_old) with its application (using ε*).
A reviewer may object that the constant C=204 is not validated against ε*.

---

## Required Fix

### Step 1: Explicit dual definition

Add the following display before or immediately after the definition of C:

```latex
\varepsilon_{\mathrm{old}}(u)
  := \sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}},
\qquad
\varepsilon_*(u) := 2\,\varepsilon_{\mathrm{old}}(u).
```

### Step 2: Clarify how C was computed

Replace:

```
C := |ΔQ| / (ε · |Q_{φ₁}|)|_{u=1} = 204,    ε(1) = 9.59×10⁻³⁰
```

With:

```latex
C_{\mathrm{old}}
:= \frac{|\Delta Q|}{\varepsilon_{\mathrm{old}}(1)\cdot|Q_{\varphi_1}(1)|}
= 204,
\qquad
\varepsilon_{\mathrm{old}}(1) = 9.59\times10^{-30},
\quad
\frac{|\Delta Q|}{|Q_{\varphi_1}|}\bigg|_{u=1} = 1.95\times10^{-27}.
```

### Step 3: Derive C* and show C=204 is conservative

Add the following sentence after the definition:

```latex
Since $\varepsilon_*(1) = 2\,\varepsilon_{\mathrm{old}}(1)$, the corrected ratio is
$$
C_* := \frac{|\Delta Q|}{\varepsilon_*(1)\cdot|Q_{\varphi_1}(1)|}
= \frac{C_{\mathrm{old}}}{2} = 102.
$$
Therefore using $C = C_{\mathrm{old}} = 204$ in the bound
$|W_{\mathrm{tail}}| \leq C\,\varepsilon_*$
is \emph{conservative by a factor of 2}: the actual ratio $C_*\,\varepsilon_* = 102\,\varepsilon_*$
is half the claimed $204\,\varepsilon_*$.
```

---

## Numerical Consistency Check

At u = 1:

| Quantity | Value |
|---|---|
| ε_old(1) | 9.59×10⁻³⁰ |
| ε*(1) = 2·ε_old(1) | 1.918×10⁻²⁹ |
| |ΔQ|/|Q_{φ₁}| at u=1 | 1.95×10⁻²⁷ |
| C_old = ratio / ε_old(1) | 1.95×10⁻²⁷ / 9.59×10⁻³⁰ ≈ 203.3 ≈ 204 |
| C* = ratio / ε*(1) | 1.95×10⁻²⁷ / 1.918×10⁻²⁹ ≈ 101.7 ≈ 102 |

Using C=204 with ε*:  C·ε*(1) = 204×1.918×10⁻²⁹ ≈ 3.91×10⁻²⁷
Actual ratio:          C*·ε*(1) = 102×1.918×10⁻²⁹ ≈ 1.96×10⁻²⁷

The bound C·ε* = 204·ε* is conservative (overshoots by factor ~2), so the conclusion
that (log Φ)'' < 0 is not affected. But the notation mismatch must be explained.

---

## Required Deliverable Text

The following sentence must appear in the paper, either in the proof of Theorem thm:extended
or in a footnote:

> Although $C = 204$ was computed using $\varepsilon_{\mathrm{old}}$,
> the corrected $\varepsilon_*$ is twice as large, so the corresponding ratio $C_*$ is half
> as large ($C_* \approx 102$). Retaining $C = 204$ in the bound
> $|W_{\mathrm{tail}}| \leq 204\,\varepsilon_*$ is therefore conservative.

---

## Acceptance Criterion

The paper must not define C using ε and then apply it to ε* without explanation.
After this fix, the reader can verify: C·ε* = 204·ε* ≥ 2·C*·ε*, so the bound is
valid (conservative) even with the factor-of-2 discrepancy in the prefactor definition.

**Status: RESOLVED** (conservative argument is rigorous; paper text must be updated).
