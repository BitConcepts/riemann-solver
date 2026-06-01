# Deliverable: github_url_linebreak_fix.md

## Problem
The repo URL may break at "riemann-solver" across lines because pdflatex
doesn't know to break at the hyphen inside a URL.

## Fix (already have xurl loaded)
The \url{} command with xurl should handle this. If still breaking,
use \path{} for the URL or wrap in \sloppy:
\begin{sloppy}
\url{https://github.com/BitConcepts/riemann-solver}
\end{sloppy}
