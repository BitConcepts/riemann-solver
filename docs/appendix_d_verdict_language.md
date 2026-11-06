# Deliverable: appendix_d_verdict_language.md
# Appendix D — Final Verdict Language Update

## Problem

The acceptance checklist currently ends with a count error ("15 of 18") and lacks
an explicit qualification about what the current state of the paper means for
submission readiness.

The paper's Section sec:limitations already says peer review is outstanding, but the
checklist verdict should mirror this directly so a reader scanning the checklist does
not form an overly optimistic impression.

---

## Required Verdict Language

The following text should appear as the final paragraph of the acceptance checklist
(§sec:checklist), replacing the current verdict line:

```latex
\noindent \textbf{Overall verdict: 14 of 18 criteria fully met, 3 not met, 1 partial.}
The work is suitable for \emph{specialist pre-review as a conditional proof package}.
It is not yet submission-ready for a top journal until the following are resolved:
\begin{itemize}[nosep]
\item P\'{o}lya source audit (C-16): direct reading of the 1927 German text is required.
\item Independent specialist review (C-6): at least two analytic number theorists.
\item Lean formalization (C-4, C-5): IA certificates and P\'{o}lya theorem machine-checked.
\end{itemize}
```

---

## Rationale

1. **"Conditional proof package"** is the accurate description: the proof is complete
   modulo cited external dependencies (Pólya's theorem, classical properties of Φ).

2. **"Not yet submission-ready for a top journal"** is honest and necessary: the CMI
   standards (AGENTS.md §1.2) require community acceptance after 2+ years of scrutiny,
   which has not happened.

3. **Explicit itemized blockers** give reviewers a clear checklist of what would need
   to change for a resubmission.

---

## What Should NOT Be Said

The verdict must not say:
- "VERDICT: RIEMANN HYPOTHESIS PROVED" — not until peer review and Pólya formalization
- "This proves the Riemann Hypothesis" — conditional only
- "15 of 18 criteria met" — incorrect count (see appendix_d_count_correction.md)

---

## Allowed Final Verdict Phrase (per AGENTS.md)

```
VERDICT: READY FOR SPECIALIST PRE-REVIEW AS CONDITIONAL PROOF PACKAGE
```

This should be stated verbatim in the checklist summary or the paper's discussion
section for clarity.

**Status: READY FOR PAPER EDIT** (verdict language finalized).
