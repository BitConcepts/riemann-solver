# Deliverable: appendix_b_table_final_formatting.md
# Appendix B (Proof Certificate Table) — Final Formatting with tabularx

## Problem

Appendix B (sec:cert) uses a fixed-width `tabular` environment. Some entries are
cramped and break awkwardly in narrow columns, particularly:

- C3 (classical properties of Φ) bundles three distinct properties in one cell
- The Script/Source column overflows for long script names
- SHA256 prefix table has narrow columns that may cause wrapping

---

## Fix 1: Main Certificate Table — Use tabularx, Split C3

### C3 Split Rationale

Currently: `C3 & $\Phi > 0$, $\Phi$ even, $\in L^1$ & Classical & CITED`

Three independent Pólya conditions (C3a: positivity, C3b: evenness, C3c: integrability)
are bundled. Splitting them:
- Enables future cross-referencing each condition independently
- Makes the checklist easier to audit (3 conditions vs 1 bundled entry)
- Brings the count in the table from 10 steps to 12, which aligns with C-1 through C-10
  in the acceptance checklist (with C3 being 3 items)

### Required LaTeX

Add to preamble (after `\usepackage{booktabs}`):

```latex
\usepackage{tabularx}
```

Replace the current certificate table in §sec:cert:

```latex
\begin{center}\small
\begin{tabularx}{\textwidth}{@{}lXllp{3.0cm}@{}}
\toprule
Step & Claim & Type & Status & Script / Source \\
\midrule
C1 & $\varphi_1 > 0$ & Lean & PROVED & \texttt{Basic.lean}: \texttt{phi1\_pos} \\
C2 & $(\log\varphi_1)'' < 0$ & Lean & PROVED & \texttt{Basic.lean}: \texttt{log\_phi1\_d2\_neg} \\
C3a & $\Phi > 0$ & Classical & CITED & \cite{csordas1989} Thm~A \\
C3b & $\Phi(-u) = \Phi(u)$ & Classical & CITED & \cite{titchmarsh1986} \S2.10 \\
C3c & $\Phi \in L^1(\mathbb{R})$ & Classical & CITED & \cite{titchmarsh1986} \S2.10 \\
C4 & $Q_\Phi < 0$ on $[0,1]$ & IA (mpmath.iv) & CERTIFIED & \texttt{verify\_logconcavity\_rigorous.py} \\
C4b & C4 reproduced independently & IA (Arb/FLINT) & CERTIFIED & \texttt{verify\_logconcavity\_arb.py} \\
C5 & $(\log\Phi)'' < 0$ on $[1,3]$ & Alg.+pert. & CERTIFIED & \texttt{verify\_ia\_1\_to\_3.py} \\
C6 & $(\log\Phi)'' < 0$ for $u\geq 3$ & Monotonicity & PROVED & \texttt{verify\_algebraic\_core.py} \\
C7 & $\Phi$ real analytic & Structural & PROVED & Weierstrass $M$-test, \S\ref{sec:phi} \\
C8 & $\Phi = O(e^{-\pi e^{2u}})$ & Structural & PROVED & \texttt{Basic.lean}: \texttt{phi1\_decay\_bound} \\
C9 & P\'{o}lya 1927 Satz~II & Cited thm. & CITED & \cite[Thm.~2.2]{csordas1989} \\
C10 & RH $\Leftrightarrow$ $\Xi$ real zeros & Cited thm. & CITED & \cite[\S2.1]{titchmarsh1986} \\
\bottomrule
\end{tabularx}
\end{center}
```

---

## Fix 2: SHA256 Hash Table — Use tabularx

Replace the SHA256 hash table:

```latex
\begin{center}\small
\begin{tabularx}{\textwidth}{@{}lXl@{}}
\toprule
Cert & Output file & SHA256 prefix (16 chars) \\
\midrule
C4 & \texttt{results/verify\_logconcavity\_rigorous.json} & \texttt{0D0841DAB32396D9\ldots} \\
C4b & \texttt{results/verify\_logconcavity\_arb.json} & \texttt{974B67CC58B96117\ldots} \\
C5 & \texttt{results/verify\_ia\_1\_to\_3.json} & \texttt{1BB9E9DECF13580C\ldots} \\
Main & \texttt{verification/proof\_certificate\_v2.json} & \texttt{8B538345D589638A\ldots} \\
\bottomrule
\end{tabularx}
\end{center}
```

The `X` column absorbs the file path, preventing overflow.

---

## Required Preamble Addition

Add after the existing `\usepackage{booktabs}` line:

```latex
\usepackage{tabularx}
```

---

## Acceptance Criterion

- C3 is split into C3a (Φ>0), C3b (Φ even), C3c (Φ∈L¹) — three distinct entries
- No table entry breaks mid-word in the rendered PDF
- SHA256 file paths do not overflow their column

**Status: READY FOR PAPER EDIT** (requires tabularx import + table replacement).
