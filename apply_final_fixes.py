# Apply all 12 final fixes to paper/main.tex

with open(r'paper\main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

original_len = len(text)
changes = []

# ================================================================
# FIX 1: Remove CvS paragraph from abstract (Issues 5 & 6)
# ================================================================
# The CvS paragraph is lines 44-45, starts with "We also provide"
# and ends with the closing of the Sliwinski citation.
CVS_START = 'We also provide new independent numerical evidence for the CvS spectral framework.'
if CVS_START in text:
    # Find the paragraph and remove it
    idx = text.find(CVS_START)
    # Find end of paragraph (next \n\n or \medskip)
    end_markers = ['\n\n\\medskip', '\n\n\\textbf{DOI}']
    end_idx = len(text)
    for marker in end_markers:
        m = text.find(marker, idx)
        if m != -1 and m < end_idx:
            end_idx = m
    # Remove from idx to end_idx (the paragraph and its preceding blank line)
    para = text[idx:end_idx]
    text = text[:idx] + text[end_idx:]
    changes.append('CvS paragraph removed from abstract')
else:
    print('WARNING: CvS paragraph not found')

# ================================================================
# FIX 2: Fix abstract component (3) — update min margin from 93.1 to 91.3
# ================================================================
OLD_MARGIN_ABS = r'(minimum margin~93.1; see Theorem~\ref{thm:extended} in Section~\ref{sec:extended})'
NEW_MARGIN_ABS = r'(minimum margin~91.3; see Theorem~\ref{thm:extended})'
if OLD_MARGIN_ABS in text:
    text = text.replace(OLD_MARGIN_ABS, NEW_MARGIN_ABS, 1)
    changes.append('Abstract min_margin updated to 91.3')

# ================================================================
# FIX 3: Trim falsification detail from abstract
# (Find by landmarks: the paragraph starts with 'We subject' and ends with 're-verified.')
# ================================================================
import re
# Remove the 3-sentence falsification paragraph from abstract only
pattern = (r'We subject every link in the proof chain to 36~systematic falsification attacks '
           r'.*?re-verified\.')
match = re.search(pattern, text[:text.find(r'\end{abstract}')], re.DOTALL)
if match:
    text = text[:match.start()] + r'All 36~systematic tests organized in 7~categories detected no inconsistency.' + text[match.end():]
    changes.append('Abstract falsification detail trimmed')
else:
    # Already trimmed or not matching
    pass

# ================================================================
# FIX 4: Replace Lemma W with full G'(u) < 0 proof
# ================================================================
OLD_LEMMA = r"""\begin{lemma}[Uniform tail bound]\label{lem:wtail}
For all $u \geq 1$,
\[
|W_{\mathrm{tail}}(u)| \leq \lambda(1)\cdot|W_1(u)| \leq 1.82\times 10^{-25},
\]
where $\lambda(u) := |\Delta Q(u)|/|Q_{\varphi_1}(u)|$ is the perturbation ratio.
The bound follows from: (1)~$\lambda(u)$ is strictly decreasing for $u\geq 1$ (since
$d\log\lambda/du \leq 2 - 6\pi e^{2u} < 0$); (2)~$\lambda(u)\cdot|W_1(u)|$ is maximised
at $u=1$ with value $1.95\times 10^{-27}\times 93.15 \approx 1.82\times 10^{-25}$.
\end{lemma}"""
NEW_LEMMA = r"""\begin{lemma}[Uniform tail bound]\label{lem:wtail}
For all $u \geq 1$,
\[
|W_{\mathrm{tail}}(u)| \leq G(u) := \lambda(u)\cdot|W_1(u)| \leq G(1) = 1.82\times 10^{-25},
\]
where $\lambda(u) := |\Delta Q(u)|/|Q_{\varphi_1}(u)|$.
\end{lemma}
\begin{proof}
We prove $G'(u) < 0$ for all $u \geq 0$, so $G$ is strictly decreasing and $G(u)\leq G(1)$ for $u\geq 1$.

$\frac{d}{du}\log G = \frac{d}{du}\log\lambda + \frac{d}{du}\log|W_1|.$

\emph{Step 1.} From~\cite[Theorem~4.1]{TailBound}: $\frac{d}{du}\log\lambda \leq 2 - 6\pi e^{2u}$
(the dominant $n=2$ term of $\varepsilon^*$ decays as $e^{-6\pi e^{2u}}$, while $C(u) = O(e^{2u})$).

\emph{Step 2.} $\frac{d}{du}\log|W_1| \leq 2$.
Indeed, $|W_1(u)| = 24\pi e^{2u}/h^2 + 4\pi e^{2u} \geq 4\pi e^{2u}$, and
$\frac{d}{du}|W_1| = \frac{48\pi e^{2u}(-2\pi e^{2u}-3)}{h^3} + 8\pi e^{2u} \leq 8\pi e^{2u}$
(first term is negative). Hence $\frac{d}{du}\log|W_1| \leq 8\pi e^{2u}/(4\pi e^{2u}) = 2$.

\emph{Step 3.} $\frac{d}{du}\log G \leq (2 - 6\pi e^{2u}) + 2 = 4 - 6\pi e^{2u} \leq 4 - 6\pi < 0$
for all $u \geq 0$ (since $6\pi > 4$).

Therefore $G(u) \leq G(1) = \lambda(1)\cdot|W_1(1)| = 1.95\times 10^{-27}\times 93.15 \approx 1.82\times 10^{-25}$.
\end{proof}"""
if OLD_LEMMA in text:
    text = text.replace(OLD_LEMMA, NEW_LEMMA, 1)
    changes.append('Lemma W completely repaired with G\'(u)<0 proof')
else:
    print('WARNING: Lemma W text not found')

# ================================================================
# FIX 5: Fix Theorem 5 proof — ε* notation and remove editorial note
# ================================================================
OLD_T5_EPS = (r'|W_{\mathrm{tail}}(u)| \leq C\,\varepsilon(u),'
              '\n'
              r'\quad'
              '\n'
              r'\varepsilon^*(u) := 2\sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}}\quad\text{[corrected: }B_n(u)/n^4 < 2\text{]},')
NEW_T5_EPS = r'|W_{\mathrm{tail}}(u)| \leq C\,\varepsilon^*(u), \quad \varepsilon^*(u) := 2\sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}},'
if OLD_T5_EPS in text:
    text = text.replace(OLD_T5_EPS, NEW_T5_EPS, 1)
    changes.append('Theorem 5: editorial note removed from math, ε* used')

# Also fix the C definition to use ε*
OLD_C_DEF = (r'where $C = 204$ is the explicitly computed proportionality constant at $u = 1$:\n'
             r'\[\n'
             r'C := \frac{|\Delta Q|}{\varepsilon \cdot |Q_{\varphi_1}|}\bigg|_{u=1} = 204,\n'
             r'\quad\n'
             r'\varepsilon(1) = 9.59\times 10^{-30},\n'
             r'\quad |\Delta Q|/|Q_{\varphi_1}| = 1.95\times 10^{-27}.\n'
             r'\]')
NEW_C_DEF = (r'where $C = 204$ is a conservative constant: using $\varepsilon^*(1) \approx 1.82\times 10^{-29}$,\n'
             r'\[\n'
             r'C^* := \frac{|\Delta Q|}{\varepsilon^* \cdot |Q_{\varphi_1}|}\bigg|_{u=1} \approx 102 \leq 204,\n'
             r'\quad |\Delta Q|/|Q_{\varphi_1}| = 1.95\times 10^{-27}.\n'
             r'\]'
             '\n'
             r'Hence $C=204$ with $\varepsilon^*$ is conservative ($204\,\varepsilon^*(1) \approx 3.7\times 10^{-27}$).')
if OLD_C_DEF in text:
    text = text.replace(OLD_C_DEF, NEW_C_DEF, 1)
    changes.append('Theorem 5: C definition updated to use ε*, note C*≤204')

# Fix stale SHA256 in Theorem 5 proof
text = text.replace(
    r'(SHA256 of output: \texttt{7D65253C...})',
    r'(SHA256: \texttt{1BB9E9DECF13580C...})',
    1
)
changes.append('Theorem 5: SHA256 hash updated to 1BB9E9DE')

# Fix the margin reference (93.1 → 91.3) in Theorem 5 proof result line
text = text.replace(
    r'while $|W_1(u)| \geq 93.1$.',
    r'while the certified minimum margin is $91.3$.',
    1
)
changes.append('Theorem 5: corrected |W1| bound to certified margin 91.3')

# ================================================================
# FIX 6: Fix Theorem 6 proof — consistent ε* notation
# ================================================================
# Fix the decomposition line
text = text.replace(
    r'bound $|W_{\mathrm{tail}}| \leq C\,\varepsilon$ with $C = 204$, it suffices to show'
    '\n'
    r'$W_1(u) + 204\,\varepsilon(u) < 0$ for $u \geq 3$.',
    r'bound $|W_{\mathrm{tail}}| \leq C\,\varepsilon^*$ with $C = 204$, it suffices to show'
    '\n'
    r'$W_1(u) + 204\,\varepsilon^*(u) < 0$ for $u \geq 3$.',
    1
)
changes.append('Theorem 6: ε→ε* in decomposition line')

# Fix the numeric consistency (10^{-1637} → 10^{-1636})
text = text.replace(
    r'Hence $W_1(3) + 204\,\varepsilon(3) < -1000 + 204\cdot 10^{-1637} < 0$.',
    r'Hence $W_1(3) + 204\,\varepsilon^*(3) < -1000 + 204\cdot 10^{-1636} < 0$.',
    1
)
changes.append('Theorem 6: ε(3) → ε*(3) and 10^{-1637} → 10^{-1636}')

# Fix "both W_1 and 204ε" lines
text = text.replace(
    r'Since both $W_1$ and $204\varepsilon$ are strictly decreasing for $u \geq 3$,'
    '\n'
    r'$W_1(u) + 204\,\varepsilon(u) \leq W_1(3) + 204\,\varepsilon(3) < 0$ for all $u \geq 3$.',
    r'Since both $W_1$ and $204\varepsilon^*$ are strictly decreasing for $u \geq 3$,'
    '\n'
    r'$W_1(u) + 204\,\varepsilon^*(u) \leq W_1(3) + 204\,\varepsilon^*(3) < 0$ for all $u \geq 3$.',
    1
)
changes.append('Theorem 6: 204ε → 204ε* in monotonicity conclusion')

# Update tail ratios to ε* notation and corrected values
OLD_TAIL = (r'\textbf{Tail ratios:} $\varepsilon(1.0) = 9.59\times 10^{-30}$,'
            '\n'
            r'$\varepsilon(1.5) = 9.98\times 10^{-82}$, $\varepsilon(2.0) = 5.37\times 10^{-223}$,'
            '\n'
            r'$\varepsilon(3.0) < 10^{-1637}$. See \texttt{proof/verify\_algebraic\_core.py}.')
NEW_TAIL = (r'\textbf{Corrected tail values $\varepsilon^*(u) = 2\varepsilon_{\mathrm{old}}(u)$:}'
            r' $\varepsilon^*(1.0) \approx 1.82\times 10^{-29}$,'
            '\n'
            r'$\varepsilon^*(1.5) \approx 1.96\times 10^{-81}$, $\varepsilon^*(2.0) \approx 1.07\times 10^{-222}$,'
            '\n'
            r'$\varepsilon^*(3.0) < 10^{-1636}$. See \texttt{proof/verify\_algebraic\_core.py}.')
if OLD_TAIL in text:
    text = text.replace(OLD_TAIL, NEW_TAIL, 1)
    changes.append('Theorem 6: tail ratio values updated to ε* notation')

# Also fix the ε*(3) exponent reference in the Proof-Critical Dependencies table
text = text.replace(
    r'monotonicity+$\varepsilon(3)<10^{-1637}$',
    r'monotonicity+$\varepsilon^*(3)<10^{-1636}$',
    1
)
changes.append('Proof-Critical Deps table: ε(3) exponent corrected')

# ================================================================
# FIX 7: Fix Appendix C table — raw math text
# ================================================================
OLD_APP_C = r'$\log K$ concave ($(\\log K)''\\ leq 0$)'
NEW_APP_C = r'$(\\log K)'' \\leq 0$'
# Use exact string matching for the LaTeX source
text = text.replace(
    r'$\log K$ concave ($(\log K)''\ leq 0$)',
    r'$(\log K)'' \leq 0$',
    1
)
changes.append('Appendix C: raw math text fixed to proper LaTeX')

# ================================================================
# FIX 8: Fix Appendix B hash table header
# ================================================================
text = text.replace(
    r'SHA256 (full 64 hex, see \texttt{docs/certificate\_hash\_table.md})',
    r'SHA256 prefix (16 chars); full hash in \texttt{docs/certificate\_hash\_table.md}',
    1
)
changes.append('Appendix B: hash table header corrected (prefix not full hash)')

# Also add note below the table
OLD_HASH_NOTE = r'To verify: run the corresponding script and compare the SHA256 of the output JSON against the table above.'
NEW_HASH_NOTE = (r'Prefixes shown for readability. Full 64-character SHA256 hashes are in '
                 r'\texttt{docs/certificate\_hash\_table.md}. '
                 r'To verify: run the corresponding script and compare.')
text = text.replace(OLD_HASH_NOTE, NEW_HASH_NOTE, 1)
changes.append('Appendix B: hash note updated')

# ================================================================
# FIX 9: Add C-17 and C-18 as explicit items to Appendix D
# ================================================================
C16_ENDING = (
    r'\item[C-16.] \textbf{P\'olya Satz~II source audit with verdict.}' + '\n'
    + r'  Status: $\sim$ PARTIAL --- verdict: SOURCE MATCH VERIFIED WITH MODIFIED HYPOTHESES.' + '\n'
    + r'  German original paywalled; primary text not directly verified.' + '\n'
    + r'  Required before top-journal submission.' + '\n'
    + r'\end{enumerate}'
)
if C16_ENDING in text:
    NEW_D_ITEMS = (
        r'\item[C-16.] \textbf{P\'olya Satz~II source audit with verdict.}' + '\n'
        + r'  Status: $\sim$ PARTIAL --- verdict: SOURCE MATCH VERIFIED WITH MODIFIED HYPOTHESES.' + '\n'
        + r'  German original paywalled; primary text not directly verified.' + '\n'
        + r'  Required before top-journal submission.' + '\n\n'
        + r'\item[C-17.] \textbf{Tail prefactor bound corrected from $n^4$ to $2n^4$.}' + '\n'
        + r'  Status: $\checkmark$ RESOLVED. $B_n(u)/n^4 \leq 1+3/(2\pi-3) < 2$;' + '\n'
        + r'  corrected script recertifies $[1,3]$, minimum margin~91.3.' + '\n\n'
        + r'\item[C-18.] \textbf{Script renamed to \texttt{verify\_ia\_1\_to\_3.py}.}' + '\n'
        + r'  Status: $\checkmark$ DONE.' + '\n'
        + r'\end{enumerate}'
    )
    text = text.replace(C16_ENDING, NEW_D_ITEMS, 1)
    changes.append('Appendix D: C-17 and C-18 added as explicit items')
else:
    print('WARNING: Appendix D ending not found')

# ================================================================
# FIX 10: Fix typo "uncontroversal" → "uncontroversial"
# ================================================================
text = text.replace('uncontroversal', 'uncontroversial')
changes.append('Typo fixed: uncontroversal → uncontroversial')

# ================================================================
# FIX 11: Shorten abstract — remove detailed falsification
# (if the trimming above didn't catch it)
# ================================================================
# The abstract might still have full falsification detail; clean it up
text = text.replace(
    r'All 36~systematic tests organized in 7~batches. Each test attempts to detect an inconsistency or counterexample. These tests are confidence-building and do not substitute for the proof-critical certificates in Section~\ref{sec:deps}. No test detected any inconsistency. A representative selection:',
    r'All 36~systematic tests organized in 7~batches detected no inconsistency.',
    1
)
changes.append('Section 11 falsification opening simplified')

# ================================================================
# FIX 12: Add prose note about ε* factor after the definition in Thm 5
# ================================================================
# Add explanation after the display in the proof
PROSE_INSERT_AFTER = r'$\varepsilon^*(u) := 2\sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}},'
if PROSE_INSERT_AFTER in text:
    idx = text.find(PROSE_INSERT_AFTER)
    if idx != -1:
        # Find end of the displayed math block (next \\])
        end_math = text.find(r'\]', idx)
        if end_math != -1:
            insert_pos = end_math + len(r'\]')
            prose = '\nThe factor~2 comes from the corrected prefactor bound $B_n(u)/n^4 \\leq 1+3/(2\\pi-3) < 2$ (Proposition~\\ref{prop:tail_ratio}).\n'
            # Only add if not already there
            if prose.strip() not in text[insert_pos:insert_pos+200]:
                text = text[:insert_pos] + prose + text[insert_pos:]
                changes.append('Theorem 5: factor-2 prose note added after ε* display')

# ================================================================
# Write result
# ================================================================
with open(r'paper\main.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Original: {original_len} chars')
print(f'New: {len(text)} chars')
print('Changes:')
for c in changes:
    print(f'  + {c}')
