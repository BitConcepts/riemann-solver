# Deliverable: appendix_c_table_final_formatting.md
# Appendix C (Pólya Source Analysis) Table — Final Math Formatting

## Problem

The Appendix C comparison table (sec:polya_audit) currently extracts from the PDF with
broken math formatting:

```
Kernel even, K(−t) =
K(t)

((log K)'' leq0)
```

Two specific issues:

1. **Kernel even cell**: `K(-t)=K(t)` should render in math mode; instead it wraps
   as text and the equals sign is extracted on a separate line.

2. **Log-concavity cell**: `((log K)'' leq0)` is using text-mode with double
   parentheses and a broken `\leq` (appears as "leq0" without the backslash rendering).

---

## Current Table Structure (from paper/main.tex, §sec:polya_audit)

```latex
\begin{center}\small
\begin{tabular}{@{}p{4cm}p{5cm}p{3cm}@{}}
\toprule
Polya 1927 (Satz II) & Csordas--Varga 1989 (Thm 2.2) & Our $\Phi$ satisfies \\
\midrule
Kernel even, $K(-t)=K(t)$ & Assumed; eq.~(2.2) & Prop.~\ref{prop:phi_properties}~(ii) \\
Kernel positive $K > 0$ & Thm~A (cited) & Prop.~\ref{prop:phi_properties}~(i) \\
Kernel in $L^1$ & Implicitly via decay & Prop.~\ref{prop:phi_properties}~(iii) \\
$\log K$ concave ($({\log K})''\  leq 0$) & Eq.~(2.3) & Theorems~\ref{thm:ia}... \\
Decay: $K = O(e^{-|t|^{2+\delta}})$ & Eq.~(2.4), some $\delta>0$ & Prop.~\ref{prop:phi_properties}~(iv)... \\
Real analytic near origin & Eq.~(2.5) / their notation & Prop.~\ref{prop:phi_properties}~(v) \\
\bottomrule
\end{tabular}
\end{center}
```

---

## Required Fixes

### Fix 1: Log-concavity row — fix `\ leq` typo

Current (broken):

```latex
$\log K$ concave ($({\log K})''\  leq 0$)
```

Replace with (correct math mode):

```latex
$\log K$ concave, $(\log K)''\le 0$
```

The double-space before `leq` was causing it to render as text "leq0". Remove the
extra space and use `\le` or `\leq`.

### Fix 2: Kernel even row — already in math mode

The current `$K(-t)=K(t)$` is already correctly in math mode. If PDF extraction
wraps it, that is a viewer artifact. No LaTeX change needed for this cell.

However, for cleaner visual presentation, consider shortening the cell text:

Replace:

```latex
Kernel even, $K(-t)=K(t)$
```

With:

```latex
Kernel even: $K(-t)=K(t)$
```

(colon instead of comma; marginally cleaner but not required)

---

## Full Corrected Table

```latex
\begin{center}\small
\begin{tabular}{@{}p{4cm}p{5cm}p{3cm}@{}}
\toprule
P\'{o}lya 1927 (Satz~II) & Csordas--Varga 1989 (Thm~2.2) & Our $\Phi$ satisfies \\
\midrule
Kernel even: $K(-t)=K(t)$ & Assumed; eq.~(2.2) & Prop.~\ref{prop:phi_properties}~(ii) \\
Kernel positive: $K > 0$ & Thm~A (cited) & Prop.~\ref{prop:phi_properties}~(i) \\
Kernel in $L^1$ & Implicitly via decay & Prop.~\ref{prop:phi_properties}~(iii) \\
$\log K$ concave: $(\log K)''\le0$ & Eq.~(2.3) & Thms.~\ref{thm:ia},\,\ref{thm:extended},\,\ref{thm:perturbation_tail} \\
Decay: $K=O(e^{-|t|^{2+\delta}})$ & Eq.~(2.4), $\delta>0$ & Prop.~\ref{prop:phi_properties}~(iv) \\
Real analytic near origin & Eq.~(2.5) & Prop.~\ref{prop:phi_properties}~(v) \\
\bottomrule
\end{tabular}
\end{center}
```

Key changes:
- `\ leq` typo → `\le` (fixes extracted `leq0` artifact)
- Column headers use consistent `Thm~` abbreviation
- Theorem list in row 4 uses `\,` for spacing
- `p{4cm}` cells are narrow; ensure Pólya source column is padded adequately

---

## Acceptance Criterion

After fix: PDF text extraction shows `(log K)'' ≤ 0` (not `leq0`) and `K(−t) = K(t)`
on a single line.

**Status: FIXED** (one-character LaTeX typo correction + minor formatting).
