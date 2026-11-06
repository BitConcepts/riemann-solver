#!/usr/bin/env python3
"""Apply remaining v7 fixes to paper/main.tex"""
import re

with open(r'D:\Development\BitConcepts\riemann-solver\paper\main.tex', 'r', encoding='utf-8') as f:
    content = f.read()

fixes_applied = []

# Fix 6: Step 3 in lem:wtail proof
old = r'\emph{Step 3.} $\frac{d}{du}\log G \leq (2 - 6\pi e^{2u}) + 2 = 4 - 6\pi e^{2u} \leq 4 - 6\pi < 0$'
new = r'\emph{Step 3.} $\frac{d}{du}\log G \leq (-6\pi e^{2u}) + 2 = 2 - 6\pi e^{2u} \leq 2 - 6\pi < 0$'
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 6a: Step 3 bound updated')

old = r'for all $u \geq 0$ (since $6\pi > 4$).'
new = r'for all $u \geq 0$ (since $6\pi > 2$).'
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 6b: 6pi>4 -> 6pi>2')

# Fix 7a: Remove inline varepsilon* := definition from thm:extended
old = r'|W_{{\mathrm{tail}}}(u)| \leq C\,\varepsilon^*(u), \quad \varepsilon^*(u) := 2\sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}},'
new = r'|W_{{\mathrm{tail}}}(u)| \leq C\,\varepsilon^*(u),'
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 7a: inline eps* def removed')

# Fix 7b: C definition using ε_old
old = r'C := \frac{|\Delta Q|}{\varepsilon \cdot |Q_{\varphi_1}|}\bigg|_{u=1} = 204,'
new = r'C_{\mathrm{old}} := \frac{|\Delta Q|}{\varepsilon_{\mathrm{old}}(1)\cdot|Q_{\varphi_1}(1)|} = 204,'
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 7b: C definition fixed')

# Fix 7c: ε(1) -> ε_old(1)
old = r'\varepsilon(1) = 9.59\times 10^{-30},'
new = r'\varepsilon_{\mathrm{old}}(1) = 9.59\times 10^{-30},'
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 7c: eps(1) -> eps_old(1)')

# Fix 7d: Add conservative note (insert after ΔQ/Q line)
old = r'\quad |\Delta Q|/|Q_{\varphi_1}| = 1.95\times 10^{-27}.'
new = (r'\quad |\Delta Q|/|Q_{\varphi_1}|\big|_{u=1} = 1.95\times 10^{-27}.' + '\n'
     + r'\]' + '\n'
     + r'Since $\varepsilon^*(1) = 2\varepsilon_{\mathrm{old}}(1)$, the corrected ratio $C_*\approx102$; retaining $C=204$ with $\varepsilon^*$ is conservative by a factor of~$2$.'
     + '\n' + r'\[')
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 7d: conservative note added')

# Fix 8: -93.1 -> -91.3
old = r'\leq -93.1 + 1.82\times 10^{-25} < 0$.'
new = r'\leq -91.3 + 1.82\times 10^{-25} < 0$.'
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 8: -93.1 -> -91.3')

# Fix 9: eps* monotonicity in thm:perturbation_tail
old = r'\emph{$\varepsilon$ is strictly decreasing.} Each term satisfies'
new = (r'\emph{$\varepsilon^*$ is strictly decreasing,} since it is twice a sum of strictly'
     + '\n'
     + r'decreasing positive terms (Lemma~\ref{sublem:lambda_decay}(a)). Each term of $\varepsilon^*$ satisfies')
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 9: eps->eps* monotonicity fixed')

# Fix 10: Update derivative to show factor of 2 for ε*
old = r'$\tfrac{d}{du}\bigl[n^4 e^{-\pi(n^2-1)e^{2u}}\bigr] = -2\pi(n^2-1)e^{2u}\cdot n^4 e^{-\pi(n^2-1)e^{2u}} < 0$'
new = r'$\tfrac{d}{du}\bigl[2n^4 e^{-\pi(n^2-1)e^{2u}}\bigr] = -4\pi(n^2-1)e^{2u}\cdot n^4 e^{-\pi(n^2-1)e^{2u}} < 0$'
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 10: derivative factor-of-2 updated')

# Fix 11: Appendix C table - fix '\ leq' typo
old = r"$\log K$ concave ($({\log K})''\  leq 0$)"
new = r"$\log K$ concave: $(\log K)''\le0$"
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 11: Appendix C leq typo fixed')

# Fix 12: Appendix B main table - switch to tabularx and split C3
old = (r'\begin{center}\small' + '\n'
     + r'\begin{tabular}{@{}llllp{3.5cm}@{}}' + '\n'
     + r'\toprule' + '\n'
     + r'Step & Claim & Type & Status & Script / Source \\' + '\n'
     + r'\midrule' + '\n'
     + r'C1 & $\varphi_1 > 0$ & Lean & PROVED & \texttt{Basic.lean}: \texttt{phi1\_pos} \\' + '\n'
     + r'C2 & $(\log\varphi_1)'' < 0$ & Lean & PROVED & \texttt{Basic.lean}: \texttt{log\_phi1\_d2\_neg} \\' + '\n'
     + r'C3 & $\Phi > 0$, $\Phi$ even, $\in L^1$ & Classical & CITED & \cite{titchmarsh1986,csordas1989} \\' + '\n'
     + r'C4 & $Q_\Phi < 0$ on $[0,1]$ & IA (mpmath.iv) & CERTIFIED & \texttt{verify\_logconcavity\_rigorous.py} \\' + '\n'
     + r'C4b & C4 reproduced & IA (Arb/FLINT) & CERTIFIED & \texttt{verify\_logconcavity\_arb.py} \\' + '\n'
     + r'C5 & $(\log\Phi)'' < 0$ on $[1,3]$ & Alg.+pert. & CERTIFIED & \texttt{verify\_ia\_1\_to\_3.py} \\' + '\n'
     + r'C6 & $(\log\Phi)'' < 0$ for $u\geq 3$ & Monotonicity & PROVED & \texttt{verify\_algebraic\_core.py} \\' + '\n'
     + r'C7 & $\Phi$ real analytic & Structural & PROVED & Weierstrass $M$-test, §\ref{sec:phi} \\' + '\n'
     + r'C8 & $\Phi = O(e^{-\pi e^{2u}})$ & Structural & PROVED & \texttt{Basic.lean}: \texttt{phi1\_decay\_bound} \\' + '\n'
     + r'C9 & P\'{o}lya 1927 Satz~II & Cited thm. & CITED & \cite[Thm.~2.2]{csordas1989} \\' + '\n'
     + r'C10 & RH $\Leftrightarrow$ $\Xi$ real zeros & Cited thm. & CITED & \cite[\S2.1]{titchmarsh1986} \\' + '\n'
     + r'\bottomrule' + '\n'
     + r'\end{tabular}' + '\n'
     + r'\end{center}')
new = (r'\begin{center}\small' + '\n'
     + r'\begin{tabularx}{\textwidth}{@{}lXllp{3.0cm}@{}}' + '\n'
     + r'\toprule' + '\n'
     + r'Step & Claim & Type & Status & Script / Source \\' + '\n'
     + r'\midrule' + '\n'
     + r'C1 & $\varphi_1 > 0$ & Lean & PROVED & \texttt{Basic.lean}: \texttt{phi1\_pos} \\' + '\n'
     + r'C2 & $(\log\varphi_1)'' < 0$ & Lean & PROVED & \texttt{Basic.lean}: \texttt{log\_phi1\_d2\_neg} \\' + '\n'
     + r'C3a & $\Phi > 0$ & Classical & CITED & \cite{csordas1989} Thm~A \\' + '\n'
     + r'C3b & $\Phi(-u)=\Phi(u)$ & Classical & CITED & \cite{titchmarsh1986} \S2.10 \\' + '\n'
     + r'C3c & $\Phi \in L^1(\mathbb{R})$ & Classical & CITED & \cite{titchmarsh1986} \S2.10 \\' + '\n'
     + r'C4 & $Q_\Phi < 0$ on $[0,1]$ & IA (mpmath.iv) & CERTIFIED & \texttt{verify\_logconcavity\_rigorous.py} \\' + '\n'
     + r'C4b & C4 reproduced & IA (Arb/FLINT) & CERTIFIED & \texttt{verify\_logconcavity\_arb.py} \\' + '\n'
     + r'C5 & $(\log\Phi)'' < 0$ on $[1,3]$ & Alg.+pert. & CERTIFIED & \texttt{verify\_ia\_1\_to\_3.py} \\' + '\n'
     + r'C6 & $(\log\Phi)'' < 0$ for $u\geq 3$ & Monotonicity & PROVED & \texttt{verify\_algebraic\_core.py} \\' + '\n'
     + r'C7 & $\Phi$ real analytic & Structural & PROVED & Weierstrass $M$-test, \S\ref{sec:phi} \\' + '\n'
     + r'C8 & $\Phi = O(e^{-\pi e^{2u}})$ & Structural & PROVED & \texttt{Basic.lean}: \texttt{phi1\_decay\_bound} \\' + '\n'
     + r'C9 & P\'{o}lya 1927 Satz~II & Cited thm. & CITED & \cite[Thm.~2.2]{csordas1989} \\' + '\n'
     + r'C10 & RH $\Leftrightarrow$ $\Xi$ real zeros & Cited thm. & CITED & \cite[\S2.1]{titchmarsh1986} \\' + '\n'
     + r'\bottomrule' + '\n'
     + r'\end{tabularx}' + '\n'
     + r'\end{center}')
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 12: Appendix B main table -> tabularx + C3 split')

# Fix 13: Appendix B SHA256 table -> tabularx
old = (r'\begin{center}\small' + '\n'
     + r'\begin{tabular}{@{}lll@{}}' + '\n'
     + r'\toprule' + '\n'
     + r'Cert & Output file & SHA256 prefix (16 chars); full hash in \texttt{docs/certificate\_hash\_table.md} \\')
new = (r'\begin{center}\small' + '\n'
     + r'\begin{tabularx}{\textwidth}{@{}lXl@{}}' + '\n'
     + r'\toprule' + '\n'
     + r'Cert & Output file & SHA256 prefix (16 chars) \\')
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 13a: SHA256 table -> tabularx')

old = r'\end{tabular}' + '\n' + r'\end{center}' + '\n' + 'Prefixes shown'
new = r'\end{tabularx}' + '\n' + r'\end{center}' + '\n' + 'Prefixes shown'
# Only replace the second occurrence (SHA256 table, not Appendix B main table)
idx = content.rfind(r'\end{tabular}' + '\n' + r'\end{center}' + '\n' + 'Prefixes')
if idx >= 0:
    content = content[:idx] + content[idx:].replace(
        r'\end{tabular}' + '\n' + r'\end{center}' + '\n' + 'Prefixes',
        r'\end{tabularx}' + '\n' + r'\end{center}' + '\n' + 'Prefixes',
        1
    )
    fixes_applied.append('Fix 13b: SHA256 table end tag -> tabularx')

# Fix 14: Appendix D count and verdict
old = (r'\noindent \textbf{Overall verdict: 15 of 18 criteria met.}' + '\n'
     + r'C-4 (Lean IA formalization), C-5 (Lean P\'{o}lya), C-6 (peer review) remain open.' + '\n'
     + r'C-16 partial (P\'{o}lya source audit via English restatements; German original unverified).' + '\n'
     + r'New items: C-17 (tail prefactor corrected from $n^4$ to $2n^4$);' + '\n'
     + r'C-18 (script renamed to \texttt{verify\_ia\_1\_to\_3.py}).')
new = (r'\noindent \textbf{Overall verdict: 14 of 18 criteria fully met; 3 not met; 1 partial.}' + '\n'
     + r'Not met: C-4 (Lean IA formalization), C-5 (Lean P\'{o}lya theorem), C-6 (specialist peer review).' + '\n'
     + r'Partial: C-16 (P\'{o}lya source audit via five consistent English restatements; German original not directly verified).' + '\n'
     + r'The work is suitable for specialist pre-review as a \emph{conditional proof package}; it is not yet' + '\n'
     + r'submission-ready for a top journal until C-6, C-16, C-4, and C-5 are resolved.')
if old in content:
    content = content.replace(old, new)
    fixes_applied.append('Fix 14: Appendix D count 15->14 and verdict updated')

with open(r'D:\Development\BitConcepts\riemann-solver\paper\main.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixes applied:")
for fix in fixes_applied:
    print(" ", fix)
print(f"\nTotal: {len(fixes_applied)} fixes")
