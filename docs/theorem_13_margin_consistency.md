# Deliverable: theorem_13_margin_consistency.md
# Theorem thm:extended Margin Inconsistency: 91.3 vs 93.1

## Problem

The proof of Theorem `thm:extended` currently states:

```
Result: All 101 interval checks certified, minimum margin 91.3 (at u=1.0,
interval [0.99,1.01]).  By Lemma lem:wtail, |W_tail(u)| ≤ 1.82×10⁻²⁵ for all
u ∈ [1,3], while the certified minimum margin is 91.3.  Hence
(log Φ)'' = W₁ + W_tail ≤ -93.1 + 1.82×10⁻²⁵ < 0.
```

The conclusion uses **-93.1** but the certified minimum margin is **91.3**.
These are different numbers, and their origins are not distinguished.

---

## Explanation of the Two Values

**91.3** is the IA-certified value:
The script evaluates `upper(W₁(I_i) + 204·ε*(I_i))` over interval I₀ = [0.99, 1.01].
Due to interval arithmetic overestimation (interval wrapping), the certified upper bound is
`≤ -91.3`, not `≤ -93.1`. This is the rigorous certified margin.

**93.1** is the analytic value of |W₁(1)|:
From `docs/uniform_wtail_bound.md`: |W₁(1)| = 93.15.
This value is algebraically derived from the formula for W₁:
```
W₁(1) = -24πe²/h(1)² - 4πe² where h(1) = 2πe² - 3 ≈ 43.35
W₁(1) ≈ -24π(7.389)/(43.35)² - 4π(7.389) ≈ -0.297 - 92.86 ≈ -93.15
```

The two values satisfy 91.3 < 93.1 because:
- The IA upper bound includes interval overestimation at the boundary
- 91.3 = -(IA upper bound of W₁([0.99,1.01]) + 204·ε*([0.99,1.01]))
- 93.1 ≈ |W₁(1)| analytically

Using -93.1 in the conclusion without explanation creates the false impression that the
IA certified a margin of 93.1.

---

## Required Fix

### Option A (Preferred): Use the IA-certified value consistently

Replace:

```latex
Hence $({\log\Phi})'' = W_1 + W_{\mathrm{tail}} \leq -93.1 + 1.82\times10^{-25}<0$.
```

With:

```latex
Hence $({\log\Phi})'' = W_1 + W_{\mathrm{tail}} \leq -91.3 + 1.82\times10^{-25}<0$.
```

The value 91.3 is the IA-certified lower bound on $|W_1(u) + C\,\varepsilon_*(u)|$
over the worst-case interval $[0.99, 1.01]$. This is the logically correct number to
cite in the conclusion.

### Option B: Separate the two bounds

If retaining -93.1 is desired (since |W₁(1)| = 93.15 is analytically computed),
expand the text to distinguish:

```latex
The IA certifies minimum margin $91.3$ (including overestimation) at $[0.99,1.01]$.
Independently, $|W_1(1)| = 24\pi e^2/h(1)^2 + 4\pi e^2 \approx 93.15 > 93.1$ (algebraic
lower bound). Combined with $|W_{\mathrm{tail}}(u)|\leq 1.82\times10^{-25}$
(Lemma~\ref{lem:wtail}):
$({\log\Phi})'' \leq -93.1 + 1.82\times10^{-25} < 0$.
```

This makes clear that the -93.1 bound comes from the algebraic formula, not the IA margin.

---

## Recommended Fix

**Option A** (use -91.3) is preferred for simplicity. The conclusion is equally valid
with -91.3 (since 91.3 ≫ 1.82×10⁻²⁵). The text then reads consistently:

```
minimum margin 91.3 ... Hence (log Φ)'' ≤ -91.3 + 1.82×10⁻²⁵ < 0.
```

---

## Paper Edit (LaTeX)

Locate in paper/main.tex:

```latex
$({\log\Phi})'' = W_1 + W_{{\mathrm{tail}}} \leq -93.1 + 1.82\times 10^{-25}<0$.
```

Replace with:

```latex
$({\log\Phi})'' = W_1 + W_{{\mathrm{tail}}} \leq -91.3 + 1.82\times 10^{-25}<0$.
```

---

## Acceptance Criterion

The margin value used in the final inequality must be ≤ the certified margin value
stated in the "Result:" line. Currently 93.1 > 91.3 (wrong direction). After fix:
91.3 ≤ 91.3 ✓.

**Status: FIXED** (single-character substitution; apply immediately to paper/main.tex).
