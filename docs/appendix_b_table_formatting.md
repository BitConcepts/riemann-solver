# Deliverable: appendix_b_table_formatting.md
# Task 9 — Improve Appendix B Certificate Table

## Required changes

1. Add lmodern and microtype to preamble for better text rendering
2. Use tabularx or p-column widths to prevent script name overflow
3. Split C3 into three rows (C3a, C3b, C3c) for Phi>0, Phi even, Phi in L1
4. Update C5 to reference verify_ia_1_to_3.py and corrected epsilon

## LaTeX replacement for Appendix B table

\begin{center}\small
\begin{tabular}{@{}p{0.5cm}p{3.0cm}p{1.8cm}p{1.0cm}p{4.0cm}@{}}
\toprule
Step & Claim & Type & Status & Script / Source \\
\midrule
C1 & $\varphi_1 > 0$ & Lean & PROVED & \texttt{phi1\_pos} \\
C2 & $(\log\varphi_1)'' < 0$ & Lean & PROVED & \texttt{log\_phi1\_d2\_neg} \\
C3a & $\Phi > 0$ & Classical & CITED & \cite{csordas1989} Thm~A \\
C3b & $\Phi$ even & Classical & CITED & \cite{titchmarsh1986} \S2.10 \\
C3c & $\Phi \in L^1$ & Classical & CITED & \cite{titchmarsh1986} \S2.10 \\
C4 & $Q_\Phi < 0$ on $[0,1]$ & IA (mpmath.iv) & CERT. & \texttt{verify\_logconcavity\_rigorous.py} \\
C4b & C4 reproduced & IA (Arb) & CERT. & \texttt{verify\_logconcavity\_arb.py} \\
C5 & $(\log\Phi)'' < 0$ on $[1,3]$ & Alg.+pert. & CERT. & \texttt{verify\_ia\_1\_to\_3.py} \\
C6 & $(\log\Phi)'' < 0$, $u\geq 3$ & Monotone & PROVED & \texttt{verify\_algebraic\_core.py} \\
C7 & $\Phi$ real analytic & Structural & PROVED & \S\ref{sec:phi} (disk proof) \\
C8 & $\Phi = O(e^{-\pi e^{2u}})$ & Structural & PROVED & \texttt{phi1\_decay\_bound} \\
C9 & Pólya 1927 Satz~II & Cited thm. & CITED & \cite{csordas1989} Thm~2.2 \\
C10 & RH $\Leftrightarrow$ $\Xi$ real zeros & Cited thm. & CITED & \cite{titchmarsh1986} \S2.1 \\
\bottomrule
\end{tabular}
\end{center}
