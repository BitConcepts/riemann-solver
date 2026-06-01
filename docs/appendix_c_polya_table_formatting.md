# Deliverable: appendix_c_polya_table_formatting.md

## Problems
1. Row: "$\log K$ concave ($( \log K)'' \ leq 0$)" — raw text in math
   Should be: "$(\log K)'' \leq 0$"
2. Row: "Kernel even, $K(-t)=K(t)$" — this is fine
3. Column widths too narrow causing wrapping

## Required LaTeX fix

Replace the problematic table row:
OLD: $\log K$ concave ($(\log K)''\ leq 0$)
NEW: $(\log K)'' \leq 0$

Use wider columns:
\begin{tabular}{@{}p{3.5cm}p{4.5cm}p{3.5cm}@{}}
