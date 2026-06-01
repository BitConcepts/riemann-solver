# Deliverable: url_path_linebreak_cleanup.md
# Task 17 — URL and Path Linebreak Cleanup

## Required additions to preamble

Add:
  \usepackage{xurl}

This allows URLs to break at more points including hyphens and underscores.

## Path formatting in tables

In Section 12 and Appendix B, long script paths like:
  verify_logconcavity_rigorous.py

should use \path{} or \texttt{} with \allowbreak hints if they overflow.

The current pdfLaTeX compilation shows Overfull hboxes in the tables. Fix by:
1. Using p{} columns instead of l columns in Section 12 table
2. Adding \footnotesize to the Section 12 table (already uses \small)
3. Breaking long names: \texttt{verify\_log\-concavity\_\-rigorous.py}

No hyperref changes needed (already included).
