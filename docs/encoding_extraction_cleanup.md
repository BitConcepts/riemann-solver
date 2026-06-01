# Deliverable: encoding_extraction_cleanup.md
# Task 16 — Encoding and Text Extraction Cleanup

## Required preamble additions

Add to preamble after existing packages:
  \usepackage{lmodern}
  \usepackage{microtype}

## Character replacements in paper source

All math inside text environments should use LaTeX:
- § already uses \S{} where needed
- Replace -- with \text{--} in math contexts if needed
- The table cells containing "(log K)'' leq 0" → "$({\log K})'' \leq 0$"

## Check for non-ASCII characters

The source currently has "Pólya" written as P\'olya (correct for pdfLaTeX).
The Appendix C table had "((log K)'' leq0)" as raw text — fixed in Task 10.

No encoding issues found in the main proof sections.
