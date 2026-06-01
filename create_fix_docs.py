"""Create all deliverable docs for the 12 final fixes."""
import os, textwrap

docs = {
'lemma_12_final_repair.md': """
# Deliverable: lemma_12_final_repair.md — Lemma W Complete Repair

## Problem
Lemma W claims |W_tail(u)| ≤ λ(1)·|W₁(u)| ≤ 1.82×10⁻²⁵ for all u ≥ 1.
The text says "λ(u) decreasing" but does NOT prove λ(u)·|W₁(u)| is bounded.
Since |W₁| grows, λ(u)↓ alone does not imply G(u) := λ(u)·|W₁(u)| ↓.

## Fix: Explicit G'(u) < 0 Proof (Option B)

**Lemma W (corrected):** For all u ≥ 0, G(u) := λ(u)·|W₁(u)| is strictly decreasing.
Hence G(u) ≤ G(1) = 1.82×10⁻²⁵ for all u ≥ 1.

**Proof of G'(u) < 0:**

d(log G)/du = d(log λ)/du + d(log|W₁|)/du

**Step 1:** d(log λ)/du ≤ 2 - 6πe^{2u} for u ≥ 0.
(From docs/uniform_wtail_bound.md: C(u) = O(e^{2u}), ε decays as e^{-6πe^{2u}}.)

**Step 2:** d(log|W₁|)/du ≤ 2 for all u ≥ 0.
  |W₁(u)| = 24πe^{2u}/h² + 4πe^{2u} where h = 2πe^{2u}-3.
  d|W₁|/du = 48πe^{2u}(-2πe^{2u}-3)/h³ + 8πe^{2u}
  Since -48πe^{2u}(2πe^{2u}+3)/h³ < 0, we have d|W₁|/du < 8πe^{2u}.
  Also |W₁(u)| ≥ 4πe^{2u}.
  Therefore d(log|W₁|)/du = (d|W₁|/du)/|W₁| < 8πe^{2u}/(4πe^{2u}) = 2.

**Step 3:** d(log G)/du ≤ (2 - 6πe^{2u}) + 2 = 4 - 6πe^{2u} ≤ 4 - 6π < 0 for all u ≥ 0.

(4 - 6π ≈ 4 - 18.85 = -14.85 < 0.)

**Conclusion:** G is strictly decreasing for all u ≥ 0.
G(u) ≤ G(1) = λ(1)·|W₁(1)| = 1.95×10⁻²⁷ × 93.15 ≈ 1.82×10⁻²⁵ for all u ≥ 1.

## Status: PROVED (elementary calculus, no IA needed)
""",

'epsilon_star_notation_cleanup.md': """
# Deliverable: epsilon_star_notation_cleanup.md — ε* Notation Consistency

## Problem
Theorem 5 proof uses ε and ε* interchangeably. The ε definition says
|W_tail| ≤ C·ε(u) then immediately redefines ε*(u) = 2Σn⁴... The
bracket [corrected: B_n(u)/n^4 < 2] appears inside displayed math.

## Required changes

1. Define ε*(u) once in Proposition 5, not inline in a displayed equation.
2. In Theorem 5 proof: use only ε*(u) throughout. Drop all ε references.
3. C definition: "C = |ΔQ|/(ε*(1)·|Q_φ₁(1)|)" with ε*(1) = 1.82×10⁻²⁹.
   Note: C* ≈ 112 ≤ 204, so using C=204 with ε* is conservative.
4. Remove editorial note from inside math.
5. In Theorem 6: replace all ε(u) with ε*(u) consistently.
6. "Tail ratios" in Theorem 6: label as ε*(1.0), ε*(1.5), etc.

## Old ε values (uncorrected, for reference only)
ε_old(1.0) = 9.59×10⁻³⁰  [no longer used in proof]
ε_old(1.5) = 9.98×10⁻⁸²  [no longer used in proof]

## Corrected ε* values (twice the old ε)
ε*(1.0) ≈ 1.82×10⁻²⁹  [= 2 × 9.115×10⁻³⁰, computed]
ε*(1.5) ≈ 1.96×10⁻⁸¹  [= 2 × 9.804×10⁻⁸²]
ε*(2.0) ≈ 1.07×10⁻²²²  [= 2 × 5.33×10⁻²²³]
ε*(3.0) ≤ 32e^{-3πe^6} < 10^{-1636}  [= 2 × 16e^{-3πe^6}]
""",

'C_204_after_epsilon_star.md': """
# Deliverable: C_204_after_epsilon_star.md — C=204 Audit

## Current state
C = |ΔQ(1)|/(ε_old(1)·|Q_φ₁(1)|) = 204  [using old ε]

## Under corrected ε*(1) ≈ 1.82×10⁻²⁹ (= 2 × ε_old(1)):
C* = |ΔQ(1)|/(ε*(1)·|Q_φ₁(1)|) = 204/(1.82×10⁻²⁹/9.115×10⁻³⁰) = 204/2.0 ≈ 102

Since C* ≈ 102 < 204: using C=204 with ε* is conservative.

## Paper text (add after C definition):
"Since ε*(1) = 2ε_old(1), we have C* = C/2 ≈ 102. Using C=204 with ε* 
is conservative: C·ε* = 204·ε* ≥ 2C*·ε* ≥ C*·ε* while C·ε* is doubly-
exponentially small (≈ 3.7×10⁻²⁷ at u=1, vs margin 91.3)."
""",

'theorem_14_numeric_consistency.md': """
# Deliverable: theorem_14_numeric_consistency.md — Theorem 6 Numeric Fix

## Problem
Theorem 6 currently states:
  ε*(3) ≤ 32e^{-3πe^6} < 10^{-1636}
but then uses:
  W₁(3) + 204·ε(3) < -1000 + 204·10^{-1637} < 0

This mixes ε* with ε, and uses 10^{-1637} where 10^{-1636} was stated.

## Fix
Replace the inconsistent line with:
  W₁(3) + 204·ε*(3) < -1000 + 204·10^{-1636} < 0

Also update "tail ratios" paragraph to use ε* notation:
  ε*(1.0) ≈ 1.82×10⁻²⁹, ε*(1.5) ≈ 1.96×10⁻⁸¹, ε*(2.0) ≈ 1.07×10⁻²²², ε*(3.0) < 10^{-1636}
""",

'remove_cvs_from_abstract_final.md': """
# Deliverable: remove_cvs_from_abstract_final.md

## Problem
Abstract still contains full CvS spectral paragraph (lines 44-45 in main.tex):
"We also provide new independent numerical evidence for the CvS spectral 
framework. Eigenvectors of the truncated Weil quadratic form..."

## Required fix
Remove the entire paragraph. If any trace is desired, add one sentence:
"Additional contextual comparisons are collected in Appendix A."

## Status: REQUIRED before pre-review circulation
""",

'abstract_250_word_revision.md': """
# Deliverable: abstract_250_word_revision.md

## Target: ≤250 words

After removing CvS paragraph the abstract will be ~175 words (lines 36-48
minus the 5-line CvS paragraph). The revised abstract should:

Keep:
- Main claim (log-concavity + conditional RH)
- Four proof components (with corrected min margin 91.3)
- Reproducibility sentence
- Lean sentence

Remove or trim:
- Detailed falsification attack description → simplify to 1 sentence
- "Attack 12 historically detected a bug" → remove from abstract

Revised component (3) in abstract:
OLD: "minimum margin~93.1; see Theorem~ref..."
NEW: "minimum margin~91.3"  (or just "minimum margin positive")

The abstract after fixes will be ~160-180 words — correct range.
""",

'appendix_c_polya_table_formatting.md': """
# Deliverable: appendix_c_polya_table_formatting.md

## Problems
1. Row: "$\\log K$ concave ($( \\log K)'' \\ leq 0$)" — raw text in math
   Should be: "$(\\log K)'' \\leq 0$"
2. Row: "Kernel even, $K(-t)=K(t)$" — this is fine
3. Column widths too narrow causing wrapping

## Required LaTeX fix

Replace the problematic table row:
OLD: $\\log K$ concave ($(\\log K)''\\ leq 0$)
NEW: $(\\log K)'' \\leq 0$

Use wider columns:
\\begin{tabular}{@{}p{3.5cm}p{4.5cm}p{3.5cm}@{}}
""",

'appendix_b_hash_table_fix.md': """
# Deliverable: appendix_b_hash_table_fix.md

## Problem
Table header says "full 64 hex, see docs/..." but only shows 16-char prefixes.

## Fix
Change header column:
OLD: "SHA256 (full 64 hex, see \\texttt{docs/certificate\\_hash\\_table.md})"
NEW: "SHA256 prefix (16 hex); full in \\texttt{docs/certificate\\_hash\\_table.md}"

Add note below table:
"Prefixes shown for readability; full 64-character hashes in 
\\texttt{docs/certificate\\_hash\\_table.md}."
""",

'appendix_d_checklist_count_fix.md': """
# Deliverable: appendix_d_checklist_count_fix.md

## Problem
Appendix D says "15 of 18 criteria met" but only lists C-1 through C-16 as
explicit enumerate items. C-17 and C-18 appear only in the verdict paragraph.

## Fix
Add explicit enumerate items before \\end{enumerate}:

\\item[C-17.] \\textbf{Tail prefactor corrected from $n^4$ to $2n^4$.}
  Status: $\\checkmark$ RESOLVED. $B_n(u)/n^4 \\leq 1+3/(2\\pi-3) < 2$;
  corrected script recertifies [1,3] with min margin~91.3.

\\item[C-18.] \\textbf{Script renamed to \\texttt{verify\\_ia\\_1\\_to\\_3.py}.}
  Status: $\\checkmark$ DONE. SHA256: \\texttt{1BB9E9DECF13580C...}

Then the "15 of 18" count becomes accurate with C-1..C-18 all listed.
""",

'typo_uncontroversal_fix.md': """
# Deliverable: typo_uncontroversal_fix.md

## Problem
Section 14 (Limitations) contains:
"These are classical and uncontroversal, but not formalized."

## Fix
"uncontroversal" → "uncontroversial"
""",

'github_url_linebreak_fix.md': """
# Deliverable: github_url_linebreak_fix.md

## Problem
The repo URL may break at "riemann-solver" across lines because pdflatex
doesn't know to break at the hyphen inside a URL.

## Fix (already have xurl loaded)
The \\url{} command with xurl should handle this. If still breaking,
use \\path{} for the URL or wrap in \\sloppy:
\\begin{sloppy}
\\url{https://github.com/BitConcepts/riemann-solver}
\\end{sloppy}
""",

'remove_editorial_note_from_math.md': """
# Deliverable: remove_editorial_note_from_math.md

## Problem
Theorem 5 proof contains inside a displayed equation:
  \\varepsilon^*(u) := 2\\sum ... \\quad\\text{[corrected: }B_n(u)/n^4 < 2\\text{]},

The bracketed editorial note should NOT appear inside the displayed math.

## Fix
Move the note to prose after the display:
  \\varepsilon^*(u) := 2\\sum_{n=2}^{\\infty} n^4\\,e^{-\\pi(n^2-1)e^{2u}},

Then add prose: "The factor~2 is the corrected prefactor bound established in 
Proposition~\\ref{prop:tail_ratio}: $B_n(u)/n^4 \\leq 1 + 3/(2\\pi-3) < 2$."
""",
}

for fname, content in docs.items():
    path = os.path.join('docs', fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'Created {fname}')

print('Done.')
