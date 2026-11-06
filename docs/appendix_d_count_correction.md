# Deliverable: appendix_d_count_correction.md
# Appendix D (Acceptance Checklist) — Corrected Criterion Count

## Problem

The paper currently says:

```
Overall verdict: 15 of 18 criteria met.
C-4 (Lean IA formalization), C-5 (Lean Pólya), C-6 (peer review) remain open.
C-16 partial (Pólya source audit via English restatements; German original unverified).
```

This is an incorrect count. The actual tally is:

| Criterion | Status | Reasoning |
|---|---|---|
| C-1 | ✓ MET | All theorems proved/cited |
| C-2 | ✓ MET | All computational claims certified |
| C-3 | ✓ MET | Lean build zero sorry |
| C-4 | × NOT MET | Lean IA certificates unformalized |
| C-5 | × NOT MET | Lean Pólya unformalized |
| C-6 | × NOT MET | No specialist peer review |
| C-7 | ✓ MET | Analytic implications conditioned |
| C-8 | ✓ MET | No OPEN entries in deps table |
| C-9 | ✓ MET | Analyticity corrected to local |
| C-10 | ✓ MET | W_tail bound proved |
| C-11 | ✓ MET | Interval coverage stated |
| C-12 | ✓ MET | Monotonicity proved |
| C-13 | ✓ MET | F(z)=2Ξ(z) justified |
| C-14 | ✓ MET | Abstract/intro conditional |
| C-15 | ✓ MET | SHA256 hashes listed |
| C-16 | ~ PARTIAL | Source audit via English only; German unverified |
| C-17 | ✓ MET | Tail prefactor 2n⁴ corrected |
| C-18 | ✓ MET | Script renamed |

**Correct count:**
- MET: C-1,2,3,7,8,9,10,11,12,13,14,15,17,18 = **14**
- NOT MET: C-4,5,6 = **3**
- PARTIAL: C-16 = **1**

Total: 14 + 3 + 1 = 18 ✓

The current paper says "15 of 18 met", which incorrectly counts C-16 (partial) as met.

---

## Required Fix

### In paper/main.tex, Appendix sec:checklist

Locate:

```latex
\noindent \textbf{Overall verdict: 15 of 18 criteria met.}
C-4 (Lean IA formalization), C-5 (Lean P\'{o}lya), C-6 (peer review) remain open.
C-16 partial (P\'{o}lya source audit via English restatements; German original unverified).
New items: C-17 (tail prefactor corrected from $n^4$ to $2n^4$);
C-18 (script renamed to \texttt{verify\_ia\_1\_to\_3.py}).
```

Replace with:

```latex
\noindent \textbf{Overall verdict: 14 of 18 criteria fully met; 3 not met; 1 partial.}
Not met: C-4 (Lean IA formalization), C-5 (Lean P\'{o}lya theorem), C-6 (specialist
peer review).
Partial: C-16 (P\'{o}lya source audit conducted via five consistent English restatements;
German original not directly verified due to paywall).
```

---

## Acceptance Criterion

The count must accurately reflect: partial ≠ met.

After fix: 14 + 3 + 1 = 18, with explicit breakdown of each category.

**Status: FIXED** (count correction only; no mathematical content changes).
