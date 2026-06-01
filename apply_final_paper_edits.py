# Final hardening paper edits
# Applies: tail prefactor fix, abstract shortening (remove CvS/Lean details),
# script rename references, Appendix B/C/D updates, falsification language softening

import re

with open(r'paper\main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

original_len = len(text)
changes = []

# ============================================================
# 1. Add lmodern and microtype to preamble (Task 16)
# ============================================================
OLD = r'\usepackage{geometry}'
NEW = r'\usepackage{geometry}' + '\n' + r'\usepackage{lmodern}' + '\n' + r'\usepackage{microtype}'
if OLD in text and r'\usepackage{lmodern}' not in text:
    text = text.replace(OLD, NEW, 1)
    changes.append('lmodern + microtype added to preamble')

# ============================================================
# 2. Add xurl to preamble (Task 17)
# ============================================================
if r'\usepackage{xurl}' not in text:
    text = text.replace(
        r'\usepackage{enumitem}',
        r'\usepackage{enumitem}' + '\n' + r'\usepackage{xurl}',
        1
    )
    changes.append('xurl added to preamble')

# ============================================================
# 3. Fix Proposition 5 tail bound (Task 1 — critical math fix)
#    Replace n^4 with 2n^4 as the valid upper bound
# ============================================================
OLD3 = (r"Each $|\varphi_n|/\varphi_1 \leq n^4 e^{-\pi(n^2-1)e^{2u}}$ by "
        r"Lemma~\ref{lem:tail_decay}. At $u = 0$ (worst case): "
        r"$\sum_{n\geq 2} n^4 e^{-\pi(n^2-1)} < 16\cdot e^{-3\pi} + 81\cdot e^{-8\pi} + \cdots < 0.003$.")
NEW3 = (r"The exact ratio is $|\varphi_n(u)|/\varphi_1(u) = B_n(u)\,e^{-\pi(n^2-1)e^{2u}}$ "
        r"where $B_n(u) = n^2 h_n(u)/h_1(u)$ and $h_n = 2\pi n^2 e^{2u}-3$. "
        r"Since $B_n(u)/n^4 \leq 1 + 3/(2\pi-3) < 2$ for all $u \geq 0$ (see "
        r"\texttt{docs/tail\_prefactor\_correction.md}), the valid upper bound is "
        r"$|\varphi_n|/\varphi_1 \leq 2n^4 e^{-\pi(n^2-1)e^{2u}}$. "
        r"At $u = 0$ (worst case): $\sum_{n\geq 2} 2n^4 e^{-\pi(n^2-1)} < 32\cdot e^{-3\pi} + "
        r"162\cdot e^{-8\pi} + \cdots < 0.006 < 1/50$.")
if OLD3 in text:
    text = text.replace(OLD3, NEW3, 1)
    changes.append('Proposition 5: tail prefactor corrected to 2n^4')
else:
    print('WARNING: Prop 5 tail bound text not found')

# ============================================================
# 4. Fix ε definition in Extended Certification section (Task 1)
# ============================================================
OLD4 = (r"\varepsilon(u) := \sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}},")
NEW4 = (r"\varepsilon^*(u) := 2\sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}}"
        r"\quad\text{[corrected: }B_n(u)/n^4 < 2\text{]},")
if OLD4 in text:
    text = text.replace(OLD4, NEW4, 1)
    changes.append('epsilon definition corrected to 2*n^4 in Extended Cert')

# ============================================================
# 5. Update Lemma W to not claim absolute max at u=1 (Task 2)
# ============================================================
OLD5 = (r"The bound follows from: (1)~$\lambda(u)$ is strictly decreasing for $u\geq 1$ (since\n"
        r"$d\log\lambda/du \leq 2 - 6\pi e^{2u} < 0$); (2)~$\lambda(u)\cdot|W_1(u)|$ is maximised\n"
        r"at $u=1$ with value $1.95\times 10^{-27}\times 93.15 \approx 1.82\times 10^{-25}$.")
NEW5 = (r"The bound follows from: (1)~$\lambda(u)$ is strictly decreasing for $u\geq 1$ "
        r"(proved: $d\log\lambda/du \leq 2 - 6\pi e^{2u} < 0$); "
        r"(2)~$\lambda(u) \leq \lambda(1) = 1.95\times 10^{-27}$ for all $u \geq 1$; "
        r"hence $|W_{\mathrm{tail}}(u)| \leq \lambda(u)|W_1(u)| \leq \lambda(1)|W_1(u)|$. "
        r"Since $\lambda(1) \ll 1$, $|W_{\mathrm{tail}}| \ll |W_1|$ throughout $[1,\infty)$. "
        r"At $u=1$: $\lambda(1) \times |W_1(1)| = 1.95\times 10^{-27} \times 93.15 \approx 1.82\times 10^{-25}$.")
if OLD5 in text:
    text = text.replace(OLD5, NEW5, 1)
    changes.append('Lemma W statement clarified (no absolute max claim)')

# ============================================================
# 6. Update minimum margin value in Theorem 5 (91.29, not 93.1)
# ============================================================
OLD6 = r"minimum margin~93.1 (at $u = 1.0$)"
NEW6 = r"minimum margin~91.3 (at $u = 1.0$, with corrected $\varepsilon^*$)"
if OLD6 in text:
    text = text.replace(OLD6, NEW6, 1)
    changes.append('Minimum margin updated to 91.3 (corrected epsilon*)')

OLD6b = r"minimum\nmargin $93.1$ (at $u = 1.0$)."
if OLD6b in text:
    text = text.replace(OLD6b, r"minimum\nmargin $91.3$ (at $u = 1.0$, corrected $\varepsilon^*$).", 1)

# Also fix the Theorem 5 result line
OLD6c = r"\textbf{Result:} All 101 interval checks certified, minimum margin $93.1$ (at $u = 1.0$,"
NEW6c = r"\textbf{Result:} All 101 interval checks certified, minimum margin $91.3$ (at $u = 1.0$,"
if OLD6c in text:
    text = text.replace(OLD6c, NEW6c, 1)
    changes.append('Theorem 5 result min_margin updated to 91.3')

# ============================================================
# 7. Update Theorem 6: ε*(3) < 10^{-1636} (not -1637)
# ============================================================
OLD7 = r"\varepsilon(3) &\leq 16\,e^{-3\pi e^6} < 10^{-1637}."
NEW7 = r"\varepsilon^*(3) &\leq 32\,e^{-3\pi e^6} < 10^{-1636}."
if OLD7 in text:
    text = text.replace(OLD7, NEW7, 1)
    changes.append('Theorem 6: epsilon*(3) bound corrected to 10^{-1636}')

# ============================================================
# 8. Update script name references (Task 12)
# ============================================================
for old, new in [
    (r'verify\_ia\_1\_to\_1\_5.py', r'verify\_ia\_1\_to\_3.py'),
    (r'verify\_ia\_1\_to\_1\_5.json', r'verify\_ia\_1\_to\_3.json'),
    (r'ia\_verification\_1\_0\_to\_1\_5', r'ia\_verification\_1\_to\_3'),
    (r'perturbation\_bound\_above\_1\_5', r'perturbation\_bound\_above\_3'),
]:
    count = text.count(old)
    if count > 0:
        text = text.replace(old, new)
        changes.append(f'Renamed {old} -> {new} ({count} occurrences)')

# ============================================================
# 9. Shorten abstract: remove CvS paragraph and Lean details (Tasks 6,7,15)
# ============================================================
# Remove the CvS paragraph from abstract
OLD9 = (r"\n\nWe also provide new independent numerical evidence for the CvS spectral framework. "
        r"Eigenvectors of the truncated Weil quadratic form $Q(c)$ computed via the reference "
        r"implementation of Groskin~\cite{groskin2026} exhibit strong $c$-invariance: overlaps "
        r"$\langle v(c), v(c')\rangle \geq 0.9999$ across all consecutive cutoff pairs at both "
        r"$N=3$ (cutoffs $c = 13,\ldots,29$) and $N=5$ (cutoffs $c = 17,\ldots,37$). Relative "
        r"eigenvector changes $\|\Delta v(c)\|/\|v(c)\|$ remain approximately constant at "
        r"$0.006$--$0.017$ with no clear power-law decay, consistent with the inverse-logarithmic "
        r"lower bound $\varepsilon(\lambda,N) \geq 1/(4\ln\lambda)$ of Sliwinski~\cite{sliwinski2026}.")
if OLD9 in text:
    text = text.replace(OLD9, '', 1)
    changes.append('CvS paragraph removed from abstract')
else:
    # Try without leading \n\n
    alt = OLD9.lstrip('\n')
    if alt in text:
        text = text.replace(alt, '', 1)
        changes.append('CvS paragraph removed from abstract (alt match)')

# Shorten the Lean details paragraph to one sentence (Tasks 6+15)
OLD10 = (r"All computational results are reproducible via publicly available Python scripts at "
         r"\repourl. A Lean~4 formalization (\texttt{lean4/RHProof/Basic.lean}) has been "
         r"machine-checked via \texttt{lake build} on leanprover/lean4:v4.16.0 with Mathlib "
         r"(commit \texttt{a6276f4c}); the build of 1{,}976 modules completes with zero errors "
         r"and zero \texttt{sorry} declarations. Six algebraic theorems are proved from Mathlib: "
         r"\texttt{h\_pos\_for\_nonneg}, \texttt{log\_h\_d2\_neg}, \texttt{log\_phi1\_d2\_neg}, "
         r"\texttt{phi\_positive\_exp}, and the newly added \texttt{phi1\_pos} ($\varphi_1(u) > 0$ "
         r"for $u \geq 0$) and \texttt{phi1\_decay\_bound} ($\varphi_1(u) \leq 2\pi e^{2u} "
         r"e^{-\pi e^{2u}}$ for $u \geq 0$). The main theorem \texttt{riemann\_hypothesis} "
         r"depends on 13 project-specific axioms and the 3 universal Lean kernel axioms "
         r"(\texttt{propext}, \texttt{Classical.choice}, \texttt{Quot.sound}).")
NEW10 = (r"All computational results are reproducible at \repourl, with certificate SHA256 hashes "
         r"in Appendix~\ref{sec:cert}. A Lean~4 formalization verifies the algebraic core with "
         r"zero \texttt{sorry} declarations; remaining dependencies are recorded as explicit "
         r"axioms (details in Section~\ref{sec:reproduce}).")
if OLD10 in text:
    text = text.replace(OLD10, NEW10, 1)
    changes.append('Abstract Lean paragraph shortened (removed code identifiers)')

# ============================================================
# 10. Update Appendix B certificate table: rename C5 entry, update hash (Task 8)
# ============================================================
OLD11 = r"C5 & $(\\log\\Phi)'' < 0$ on $[1,3]$ & Alg.+pert. & CERTIFIED & \texttt{verify\_ia\_1\_to\_3.py} \\"
# It was already renamed above; just update the hash reference
OLD11b = r"C5  (verify_ia_1_to_3.json):             7D65253C5A8FA397..."
NEW11b = r"C5  (verify_ia_1_to_3.json):             1BB9E9DECF13580C..."
if OLD11b in text:
    text = text.replace(OLD11b, NEW11b, 1)
    changes.append('Appendix B: C5 hash updated to 1BB9E9DECF13580C')

# Update the hash table references in Appendix B
OLD_HASH = r"\texttt{7D65253C5A8FA397...} \\"
NEW_HASH = r"\texttt{1BB9E9DECF13580C...} \\"
if OLD_HASH in text:
    text = text.replace(OLD_HASH, NEW_HASH, 1)
    changes.append('Appendix B: inline C5 hash updated')

# ============================================================
# 11. Fix Appendix C table: use proper math notation (Task 10)
# ============================================================
OLD12 = r"$\log K$ concave ($(\\log K)''\\ leq 0$)"
NEW12 = r"$(\\log K)'' \\leq 0$"
if OLD12 in text:
    text = text.replace(OLD12, NEW12, 1)
    changes.append('Appendix C: fixed (log K)'' notation')

# ============================================================
# 12. Soften falsification language (Task 19)
# ============================================================
OLD13 = (r"We subjected every link in the proof chain to 36~systematic falsification attacks "
         r"organized in 7~batches. Each attack attempts to \emph{break} the proof by finding "
         r"a counterexample or inconsistency. All 36~attacks failed. A representative selection:")
NEW13 = (r"We subjected every link in the proof chain to 36~systematic tests organized in "
         r"7~batches. Each test attempts to detect an inconsistency or counterexample. "
         r"These tests are confidence-building and do not substitute for the proof-critical "
         r"certificates in Section~\ref{sec:deps}. "
         r"No test detected any inconsistency. A representative selection:")
if OLD13 in text:
    text = text.replace(OLD13, NEW13, 1)
    changes.append('Falsification language softened (Task 19)')

OLD13b = r"All attacks fail, including:"
if OLD13b in text:
    text = text.replace(OLD13b, r"No test detected an inconsistency, including:", 1)
    changes.append('Abstract: falsification language softened')

# ============================================================
# 13. Update Appendix D verdict (Tasks 18+20)
# ============================================================
OLD14 = (r"\noindent \textbf{Overall verdict:} 13 of 16 criteria fully met; C-4, C-5, C-6 open "
         r"(Lean formalization and peer review); C-16 partial. The proof is computationally "
         r"well-founded and analytically structured for specialist peer review.")
NEW14 = (r"\noindent \textbf{Overall verdict: 15 of 18 criteria met.} "
         r"C-4 (Lean IA formalization), C-5 (Lean P\\'olya), C-6 (peer review) remain open. "
         r"C-16 partial (Pólya source audit via English restatements; German original unverified). "
         r"New in this revision: C-17 (tail prefactor corrected to $2n^4$, C-18 (script renamed "
         r"to \\texttt{verify\\_ia\\_1\\_to\\_3.py}).")
if OLD14 in text:
    text = text.replace(OLD14, NEW14, 1)
    changes.append('Appendix D final verdict updated to 15/18')

# ============================================================
# 14. Add C-17 and C-18 items to Appendix D checklist
# ============================================================
OLD15 = (r"\item[C-16.] \textbf{P\\'olya Satz~II source audit with verdict.}\n"
         r"  Status: $\\sim$ PARTIAL --- verdict: SOURCE MATCH VERIFIED WITH MODIFIED HYPOTHESES.\n"
         r"  German original paywalled; primary text not directly verified.\n"
         r"  Required before top-journal submission.")
NEW15 = (r"\item[C-16.] \textbf{P\\'olya Satz~II source audit with verdict.}\n"
         r"  Status: $\sim$ PARTIAL --- verdict: SOURCE MATCH VERIFIED WITH MODIFIED HYPOTHESES.\n"
         r"  German original paywalled; primary text not directly verified.\n"
         r"  Required before top-journal submission.\n\n"
         r"\item[C-17.] \textbf{Tail prefactor bound corrected from $n^4$ to $2n^4$.}\n"
         r"  Status: $\checkmark$ RESOLVED. Exact ratio $B_n(u)/n^4 \leq 1.915 < 2$ for all $u \geq 0$;\n"
         r"  corrected script \\texttt{verify\\_ia\\_1\\_to\\_3.py} recertifies [1,3] with min margin~91.3.\n\n"
         r"\item[C-18.] \textbf{Script renamed to \\texttt{verify\\_ia\\_1\\_to\\_3.py}.}\n"
         r"  Status: $\checkmark$ DONE. SHA256: \\texttt{1BB9E9DECF13580C...} "
         r"(see Appendix~\\ref{sec:cert}).")
if OLD15 in text:
    text = text.replace(OLD15, NEW15, 1)
    changes.append('Appendix D: C-17 and C-18 items added')

# ============================================================
# 15. Update Section 12 Reproducibility table: rename script
# ============================================================
# Already done by the global replace in step 8, but also update the Lean axiom text
OLD16 = r"\texttt{ia\_verification\_1\_0\_to\_1\_5}"
if OLD16 in text:
    text = text.replace(OLD16, r"\texttt{ia\_verification\_1\_to\_3}", 1)
    changes.append('Section 12: Lean axiom name updated')

# ============================================================
# Write out
# ============================================================
with open(r'paper\main.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Original length: {original_len}')
print(f'New length: {len(text)}')
print('Changes applied:')
for c in changes:
    print(f'  + {c}')
if not changes:
    print('  (no changes — check warnings above)')
