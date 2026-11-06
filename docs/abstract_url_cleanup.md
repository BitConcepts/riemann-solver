# Deliverable: abstract_url_cleanup.md
# Abstract GitHub URL — Fix for Journal-Style Presentation

## Problem

The abstract currently ends with:

```latex
All computational results are reproducible at \repourl, with certificate SHA256
hashes in Appendix~\ref{sec:cert}.
```

Where `\repourl` expands to `\url{https://github.com/BitConcepts/riemann-solver}`.

In PDF extraction, this URL breaks as:
```
https://github.com/BitConcepts/riemann
-solver
```

Additionally, bare URLs in journal paper abstracts are nonstandard and typically
removed by editorial staff during typesetting.

---

## Package Status

The paper already loads `\usepackage{xurl}` (line 11 of main.tex) and `\usepackage{hyperref}`
(line 8). The `xurl` package should prevent line-break artifacts in the PDF.

The breaking observed in PDF extraction is a text-layer issue, not a visual one: `xurl`
places break opportunities at slashes and hyphens, so the PDF viewer may extract the
text as broken even though the rendered line is intact.

---

## Recommended Fix (Preferred): Remove URL from abstract

For a journal-style paper, the abstract should not contain a raw URL.

**Replace** the last sentence of the abstract:

```latex
All computational results are reproducible at \repourl, with certificate SHA256
hashes in Appendix~\ref{sec:cert}.
```

**With:**

```latex
All computational results are reproducible from the public repository listed in
Section~\ref{sec:reproduce}, with certificate SHA256 hashes in Appendix~\ref{sec:cert}.
```

The full URL remains in Section sec:reproduce (reproducibility section), which is
the appropriate place for it in a journal submission.

---

## Alternative Fix: LaTeX-only (if URL must stay)

If the URL must remain in the abstract, ensure the `\repourl` command uses `\url{}`
wrapped in `\texttt{}` for consistent rendering, and confirm `xurl` is loaded:

```latex
% Already in preamble — verify both are present:
\usepackage{hyperref}
\usepackage{xurl}

% Command definition — confirm:
\newcommand{\repourl}{\url{https://github.com/BitConcepts/riemann-solver}}
```

The `xurl` package inserts break-after-hyphen opportunities; the `-solver` split is
expected behavior. No further action needed for the rendered PDF. The extraction
artifact can be accepted as-is if URL in abstract is retained.

---

## Acceptance Criterion

Preferred: URL removed from abstract, cross-reference to sec:reproduce retained.
Acceptable: URL stays but is not described as "broken" since xurl handles rendering.

**Status: READY FOR PAPER EDIT**.
