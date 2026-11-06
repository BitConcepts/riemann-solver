# Deliverable: remark_2_analyticity_phrase_fix.md
# Remark 2 — Fix "Uniformly Convergent Series of Analytic Functions" Phrase

## Problem

The first Remark (containing the e^{-|t|³} counterexample) ends with:

```latex
Our kernel $\Phi$ is real analytic on all of $\mathbb{R}$
(being a uniformly convergent series of analytic functions)
and decays as $e^{-\pi e^{2u}}$, which satisfies~(iv) with any~$\delta > 0$.
```

The parenthetical "being a uniformly convergent series of analytic functions" is
**potentially misleading** because:

1. A uniformly convergent series of analytic functions on a real interval is indeed
   real analytic. However, the phrasing suggests the series converges uniformly on
   all of ℝ, which it does not (it converges uniformly only on compacts).

2. More importantly, earlier versions of this paper claimed Φ was entire by this
   same "uniform convergence" reasoning — a claim that was found to be incorrect
   (Φ is not entire; see Proposition prop:phi_properties). Retaining the phrase
   creates a false sense of déjà vu for reviewers familiar with the earlier
   (incorrect) versions.

3. The correct argument is the local Weierstrass M-test on disks of radius π/8,
   established rigorously in Proposition prop:phi_properties(v).

---

## Required Fix

### In the paper (paper/main.tex)

Locate in the first `\begin{remark}...\end{remark}` block:

```latex
Our kernel~$\Phi$ is real analytic on all of~$\mathbb{R}$ (being a uniformly convergent
series of analytic functions) and decays as $e^{-\pi e^{2u}}$, which satisfies~(iv)
with any~$\delta > 0$.
```

Replace with:

```latex
Our kernel~$\Phi$ is real analytic on~$\mathbb{R}$ by the local Weierstrass
argument in Proposition~\ref{prop:phi_properties}~(v), and decays as $e^{-\pi e^{2u}}$,
which satisfies~(iv) with any~$\delta > 0$.
```

---

## Why This Fix Is Important

The reference to Proposition prop:phi_properties(v) is:
1. **Accurate**: It correctly identifies the local disk argument (r = π/8) as the source.
2. **Traceable**: A reviewer can look up the explicit proof in §sec:phi.
3. **Conservative**: It avoids overstating global uniform convergence on ℂ, which fails.

The phrase "uniformly convergent series of analytic functions" was the exact error in
the earlier version that claimed Φ was entire. Its presence in the current remark is
a residual risk.

---

## Acceptance Criterion

The remark must reference Proposition prop:phi_properties(v) for analyticity of Φ,
not assert it via a compressed parenthetical about uniform convergence.

**Status: FIXED** (one-sentence replacement; apply to paper/main.tex).
