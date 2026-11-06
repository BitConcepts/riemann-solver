#!/usr/bin/env python3
"""Apply final remaining fixes: leq typo, C3 split, Appendix D"""

with open(r'D:\Development\BitConcepts\riemann-solver\paper\main.tex', 'r', encoding='utf-8') as f:
    content = f.read()

fixes = []

# Detect line endings
crlf = '\r\n' in content
NL = '\r\n' if crlf else '\n'
print(f"Line endings: {'CRLF' if crlf else 'LF'}")

# Fix 11: Appendix C leq typo
# Search broadly first
import re
m = re.search(r'\$\\log K\$[^\n]*leq[^\n]*', content)
if m:
    found = m.group()
    print(f"Found leq line: {repr(found[:70])}")
    old11 = found
    new11 = re.sub(r'\([^\)]*leq 0\$\)', r'$(\log K)\'\'\\le0$', found)
    # simpler: just replace the specific pattern
    new11 = re.sub(r"\(\$\(\\log K\)''\\\\ leq 0\$\)", r": $(\log K)''\\le0$", found)
    new11 = re.sub(r"\(\$\(\\log K\)''\\  leq 0\$\)", r": $(\log K)''\\le0$", found)
    # direct replace
    for variant in [r"$(\log K)''\\ leq 0$)", r"$(\log K)''\\  leq 0$)"]:
        if variant in content:
            old_full = m.group()
            new_full = old_full.replace(variant, r"$(\log K)''\\le0$")
            # Actually replace the whole concave cell
            content = content.replace(
                r"$\log K$ concave ($(\log K)''\\ leq 0$)",
                r"$\log K$ concave: $(\log K)''\\le0$"
            )
            fixes.append(f"Fix 11 (variant: {repr(variant[:20])})")
            break
    # Fallback: regex replace
    before = content
    content = re.sub(
        r"\$\\log K\$ concave \(\$\(\\log K\)''\\+\s+leq 0\$\)",
        r"$\\log K$ concave: $(\\log K)''\\le0$",
        content
    )
    if content != before:
        fixes.append("Fix 11: leq typo via regex")

# Check if C3 split needed
if "C3 & $\\Phi > 0$" in content:
    # Build search carefully with exact line endings
    lines = ["\\begin{center}\\small",
             "\\begin{tabular}{@{}llllp{3.5cm}@{}}",
             "\\toprule",
             "Step & Claim & Type & Status & Script / Source \\\\",
             "\\midrule",
             "C1 & $\\varphi_1 > 0$ & Lean & PROVED & \\texttt{Basic.lean}: \\texttt{phi1\\_pos} \\\\",
             "C2 & $(\\log\\varphi_1)'' < 0$ & Lean & PROVED & \\texttt{Basic.lean}: \\texttt{log\\_phi1\\_d2\\_neg} \\\\",
             "C3 & $\\Phi > 0$, $\\Phi$ even, $\\in L^1$ & Classical & CITED & \\cite{titchmarsh1986,csordas1989} \\\\",
             "C4 & $Q_\\Phi < 0$ on $[0,1]$ & IA (mpmath.iv) & CERTIFIED & \\texttt{verify\\_logconcavity\\_rigorous.py} \\\\",
             "C4b & C4 reproduced & IA (Arb/FLINT) & CERTIFIED & \\texttt{verify\\_logconcavity\\_arb.py} \\\\",
             "C5 & $(\\log\\Phi)'' < 0$ on $[1,3]$ & Alg.+pert. & CERTIFIED & \\texttt{verify\\_ia\\_1\\_to\\_3.py} \\\\",
             "C6 & $(\\log\\Phi)'' < 0$ for $u\\geq 3$ & Monotonicity & PROVED & \\texttt{verify\\_algebraic\\_core.py} \\\\",
             "C7 & $\\Phi$ real analytic & Structural & PROVED & Weierstrass $M$-test, \u00a7\\ref{sec:phi} \\\\",
             "C8 & $\\Phi = O(e^{-\\pi e^{2u}})$ & Structural & PROVED & \\texttt{Basic.lean}: \\texttt{phi1\\_decay\\_bound} \\\\",
             "C9 & P\\'olya 1927 Satz~II & Cited thm. & CITED & \\cite[Thm.~2.2]{csordas1989} \\\\",
             "C10 & RH $\\Leftrightarrow$ $\\Xi$ real zeros & Cited thm. & CITED & \\cite[\\S2.1]{titchmarsh1986} \\\\",
             "\\bottomrule",
             "\\end{tabular}",
             "\\end{center}"]
    new_lines = ["\\begin{center}\\small",
                 "\\begin{tabularx}{\\textwidth}{@{}lXllp{3.0cm}@{}}",
                 "\\toprule",
                 "Step & Claim & Type & Status & Script / Source \\\\",
                 "\\midrule",
                 "C1 & $\\varphi_1 > 0$ & Lean & PROVED & \\texttt{Basic.lean}: \\texttt{phi1\\_pos} \\\\",
                 "C2 & $(\\log\\varphi_1)'' < 0$ & Lean & PROVED & \\texttt{Basic.lean}: \\texttt{log\\_phi1\\_d2\\_neg} \\\\",
                 "C3a & $\\Phi > 0$ & Classical & CITED & \\cite{csordas1989} Thm~A \\\\",
                 "C3b & $\\Phi(-u)=\\Phi(u)$ & Classical & CITED & \\cite{titchmarsh1986} \\S2.10 \\\\",
                 "C3c & $\\Phi \\in L^1(\\mathbb{R})$ & Classical & CITED & \\cite{titchmarsh1986} \\S2.10 \\\\",
                 "C4 & $Q_\\Phi < 0$ on $[0,1]$ & IA (mpmath.iv) & CERTIFIED & \\texttt{verify\\_logconcavity\\_rigorous.py} \\\\",
                 "C4b & C4 reproduced & IA (Arb/FLINT) & CERTIFIED & \\texttt{verify\\_logconcavity\\_arb.py} \\\\",
                 "C5 & $(\\log\\Phi)'' < 0$ on $[1,3]$ & Alg.+pert. & CERTIFIED & \\texttt{verify\\_ia\\_1\\_to\\_3.py} \\\\",
                 "C6 & $(\\log\\Phi)'' < 0$ for $u\\geq 3$ & Monotonicity & PROVED & \\texttt{verify\\_algebraic\\_core.py} \\\\",
                 "C7 & $\\Phi$ real analytic & Structural & PROVED & Weierstrass $M$-test, \\S\\ref{sec:phi} \\\\",
                 "C8 & $\\Phi = O(e^{-\\pi e^{2u}})$ & Structural & PROVED & \\texttt{Basic.lean}: \\texttt{phi1\\_decay\\_bound} \\\\",
                 "C9 & P\\'olya 1927 Satz~II & Cited thm. & CITED & \\cite[Thm.~2.2]{csordas1989} \\\\",
                 "C10 & RH $\\Leftrightarrow$ $\\Xi$ real zeros & Cited thm. & CITED & \\cite[\\S2.1]{titchmarsh1986} \\\\",
                 "\\bottomrule",
                 "\\end{tabularx}",
                 "\\end{center}"]

    for nl in ['\n', '\r\n']:
        old12 = nl.join(lines)
        if old12 in content:
            new12 = nl.join(new_lines)
            content = content.replace(old12, new12)
            fixes.append(f"Fix 12: tabularx + C3 split (NL={repr(nl)})")
            break
    else:
        print("WARNING: Certificate table not found. Checking fragments...")
        if "\\begin{tabular}{@{}llllp{3.5cm}@{}}" in content:
            # Do targeted replacements
            content = content.replace(
                "\\begin{tabular}{@{}llllp{3.5cm}@{}}",
                "\\begin{tabularx}{\\textwidth}{@{}lXllp{3.0cm}@{}}"
            )
            content = content.replace(
                "C3 & $\\Phi > 0$, $\\Phi$ even, $\\in L^1$ & Classical & CITED & \\cite{titchmarsh1986,csordas1989} \\\\",
                "C3a & $\\Phi > 0$ & Classical & CITED & \\cite{csordas1989} Thm~A \\\\\nC3b & $\\Phi(-u)=\\Phi(u)$ & Classical & CITED & \\cite{titchmarsh1986} \\S2.10 \\\\\nC3c & $\\Phi \\in L^1(\\mathbb{R})$ & Classical & CITED & \\cite{titchmarsh1986} \\S2.10 \\\\"
            )
            content = content.replace(
                "C7 & $\\Phi$ real analytic & Structural & PROVED & Weierstrass $M$-test, \u00a7\\ref{sec:phi} \\\\",
                "C7 & $\\Phi$ real analytic & Structural & PROVED & Weierstrass $M$-test, \\S\\ref{sec:phi} \\\\"
            )
            # Find the matching \end{tabular} in the cert section
            idx = content.find("\\end{tabularx}")
            cert_end = content.find("\\end{tabular}", content.find("\\begin{tabularx}{\\textwidth}{@{}lXllp{3.0cm}@{}}"))
            if cert_end > 0 and content[cert_end:cert_end+14] != "\\end{tabularx}":
                content = content[:cert_end] + "\\end{tabularx}" + content[cert_end+len("\\end{tabular}"):]
            fixes.append("Fix 12: targeted cert table replacements")

# Fix 14: Appendix D verdict
if "Overall verdict: 15 of 18 criteria met." in content:
    for nl in ['\n', '\r\n']:
        old14 = (f"\\noindent \\textbf{{Overall verdict: 15 of 18 criteria met.}}{nl}"
                 f"C-4 (Lean IA formalization), C-5 (Lean P\\'olya), C-6 (peer review) remain open.{nl}"
                 f"C-16 partial (P\\'olya source audit via English restatements; German original unverified).{nl}"
                 f"New items: C-17 (tail prefactor corrected from $n^4$ to $2n^4$);{nl}"
                 f"C-18 (script renamed to \\texttt{{verify\\_ia\\_1\\_to\\_3.py}}).")
        if old14 in content:
            new14 = (f"\\noindent \\textbf{{Overall verdict: 14 of 18 criteria fully met; 3 not met; 1 partial.}}{nl}"
                     f"Not met: C-4 (Lean IA formalization), C-5 (Lean P\\'olya theorem), C-6 (specialist peer review).{nl}"
                     f"Partial: C-16 (P\\'olya source audit via five consistent English restatements; German original not directly verified).{nl}"
                     f"The work is suitable for specialist pre-review as a \\emph{{conditional proof package}}; it is not yet{nl}"
                     f"submission-ready for a top journal until C-6, C-16, C-4, and C-5 are resolved.")
            content = content.replace(old14, new14)
            fixes.append(f"Fix 14: Appendix D count+verdict (NL={repr(nl)})")
            break
    else:
        # Fallback: line-by-line
        content = content.replace(
            "\\noindent \\textbf{Overall verdict: 15 of 18 criteria met.}",
            "\\noindent \\textbf{Overall verdict: 14 of 18 criteria fully met; 3 not met; 1 partial.}"
        )
        fixes.append("Fix 14 partial: changed count to 14")

with open(r'D:\Development\BitConcepts\riemann-solver\paper\main.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFixes applied:")
for fix in fixes:
    print(" ", fix)
print(f"\nTotal: {len(fixes)} fixes")
