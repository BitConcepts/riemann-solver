# Deliverable: appendix_c_table_formatting.md
# Task 10 — Fix Appendix C Pólya Table Formatting

## Required LaTeX fix

Use a wider table and proper math in all cells.

\begin{center}\small
\begin{tabular}{@{}p{3.5cm}p{4.5cm}p{3.5cm}@{}}
\toprule
Pólya 1927 (Satz II) & Csordas--Varga 1989 (Thm~2.2) & Our $\Phi$ satisfies \\
\midrule
$K(-t)=K(t)$ (even) & Assumed; their eq.~(2.2) & Prop.~\ref{prop:phi_properties}~(ii) \\
$K(t) > 0$ & Thm~A (cited) & Prop.~\ref{prop:phi_properties}~(i) \\
$K \in L^1$ & Implicitly via decay & Prop.~\ref{prop:phi_properties}~(iii) \\
$(\log K)'' \leq 0$ & Their eq.~(2.3) & Thms~\ref{thm:ia},~\ref{thm:extended},~\ref{thm:perturbation_tail} \\
$K = O(e^{-|t|^{2+\delta}})$ & Eq.~(2.4), $\delta>0$ & Prop.~\ref{prop:phi_properties}~(iv), $\delta=1$ \\
$K$ real analytic near $0$ & Eq.~(2.5) & Prop.~\ref{prop:phi_properties}~(v) \\
\bottomrule
\end{tabular}
\end{center}

Note: Remove raw text like "(log K)'' leq 0" — replace all with LaTeX math.
