#!/usr/bin/env python3
"""Apply last 3 fixes: leq typo (Fix11), C3 split (Fix12), Appendix D (Fix14)"""

with open(r'D:\Development\BitConcepts\riemann-solver\paper\main.tex', 'r', encoding='utf-8') as f:
    content = f.read()

fixes = []

BS = chr(0x5c)   # backslash
DQ = chr(0x24)   # dollar sign $

# ---- Fix 11: Appendix C leq typo ----
# File contains: $\log K$ concave ($(\log K)''\  leq 0$)
# Hex: 0x5c (before leq) = backslash, 0x20 = space
old11 = (DQ + BS + "log K" + DQ + " concave ("
         + DQ + "(" + BS + "log K)" + "''" + BS + " leq 0" + DQ + ")")
new11 = (DQ + BS + "log K" + DQ + " concave: "
         + DQ + "(" + BS + "log K)''" + BS + "le0" + DQ)
if old11 in content:
    content = content.replace(old11, new11)
    fixes.append("Fix 11: leq typo fixed")
else:
    print(f"Fix 11 not found, old11={repr(old11)}")

# ---- Fix 12a: tabular -> tabularx in cert table ----
old12a = BS + "begin{tabular}{@{}llllp{3.5cm}@{}}"
new12a = BS + "begin{tabularx}{" + BS + "textwidth}{@{}lXllp{3.0cm}@{}}"
if old12a in content:
    content = content.replace(old12a, new12a)
    fixes.append("Fix 12a: tabular->tabularx")
else:
    print("Fix 12a: tabular spec not found (may already be fixed)")

# ---- Fix 12b: Split C3 into C3a/C3b/C3c ----
# C3 & $\Phi > 0$, $\Phi$ even, $\in L^1$ & Classical & CITED & \cite{titchmarsh1986,csordas1989} \\
old12b = ("C3 & " + DQ + BS + "Phi > 0" + DQ + ", " + DQ + BS + "Phi" + DQ +
          " even, " + DQ + BS + "in L^1" + DQ + " & Classical & CITED & " +
          BS + "cite{titchmarsh1986,csordas1989} " + BS + BS)
new12b = ("C3a & " + DQ + BS + "Phi > 0" + DQ + " & Classical & CITED & " +
          BS + "cite{csordas1989} Thm~A " + BS + BS + "\n" +
          "C3b & " + DQ + BS + "Phi(-u)=" + BS + "Phi(u)" + DQ +
          " & Classical & CITED & " + BS + "cite{titchmarsh1986} " + BS + "S2.10 " + BS + BS + "\n" +
          "C3c & " + DQ + BS + "Phi " + BS + "in L^1(" + BS + "mathbb{R})" + DQ +
          " & Classical & CITED & " + BS + "cite{titchmarsh1986} " + BS + "S2.10 " + BS + BS)
if old12b in content:
    content = content.replace(old12b, new12b)
    fixes.append("Fix 12b: C3 split into C3a/b/c")
else:
    print(f"Fix 12b: C3 not found, searching...")
    if "C3 & " in content:
        idx = content.find("C3 & ")
        print(f"  C3 at {idx}: {repr(content[idx:idx+80])}")

# ---- Fix 12c: end{tabular} -> end{tabularx} in cert section ----
# Find the tabularx section and update its end tag
idx_cert_start = content.find(new12a)
if idx_cert_start < 0:
    idx_cert_start = content.find(BS + "begin{tabularx}{" + BS + "textwidth}{@{}lXllp{3.0cm}@{}}")
if idx_cert_start > 0:
    idx_end = content.find(BS + "end{tabular}", idx_cert_start)
    expected_tabularx_end = BS + "end{tabularx}"
    if idx_end > 0 and content[idx_end:idx_end + len(expected_tabularx_end)] != expected_tabularx_end:
        content = content[:idx_end] + expected_tabularx_end + content[idx_end + len(BS + "end{tabular}"):]
        fixes.append("Fix 12c: end{tabular}->end{tabularx}")

# Fix C7 section sign (Unicode § -> LaTeX \S)
old_sec = ("C7 & " + DQ + BS + "Phi$ real analytic & Structural & PROVED & "
           "Weierstrass $M$-test, \u00a7" + BS + "ref{sec:phi} " + BS + BS)
new_sec = ("C7 & " + DQ + BS + "Phi$ real analytic & Structural & PROVED & "
           "Weierstrass $M$-test, " + BS + "S" + BS + "ref{sec:phi} " + BS + BS)
if old_sec in content:
    content = content.replace(old_sec, new_sec)
    fixes.append("Fix 12d: C7 section sign unicode->LaTeX")

# ---- Fix 14: Appendix D verdict ----
if "Overall verdict: 15 of 18 criteria met." in content:
    content = content.replace(
        BS + "noindent " + BS + "textbf{Overall verdict: 15 of 18 criteria met.}",
        BS + "noindent " + BS + "textbf{Overall verdict: 14 of 18 criteria fully met; 3 not met; 1 partial.}"
    )
    # Replace the following lines
    content = content.replace(
        "C-4 (Lean IA formalization), C-5 (Lean P" + BS + "'olya), C-6 (peer review) remain open.",
        "Not met: C-4 (Lean IA), C-5 (Lean P" + BS + "'olya theorem), C-6 (peer review)."
    )
    content = content.replace(
        "C-16 partial (P" + BS + "'olya source audit via English restatements; German original unverified).",
        "Partial: C-16 (P" + BS + "'olya audit via five consistent English restatements; German original not directly verified)."
    )
    content = content.replace(
        "New items: C-17 (tail prefactor corrected from " + DQ + "n^4" + DQ + " to " + DQ + "2n^4" + DQ + ");\n"
        + "C-18 (script renamed to " + BS + "texttt{verify" + BS + "_ia" + BS + "_1" + BS + "_to" + BS + "_3.py}).",
        "The work is suitable for specialist pre-review as a " + BS + "emph{conditional proof package};\n"
        + "not yet submission-ready for a top journal until C-6, C-16, C-4, and C-5 are resolved."
    )
    fixes.append("Fix 14: Appendix D count + verdict")

with open(r'D:\Development\BitConcepts\riemann-solver\paper\main.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixes applied:")
for fix in fixes:
    print(" ", fix)
print(f"\nTotal: {len(fixes)} fixes")
