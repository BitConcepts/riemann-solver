# Deliverable: appendix_d_checklist_count_fix.md

## Problem
Appendix D says "15 of 18 criteria met" but only lists C-1 through C-16 as
explicit enumerate items. C-17 and C-18 appear only in the verdict paragraph.

## Fix
Add explicit enumerate items before \end{enumerate}:

\item[C-17.] \textbf{Tail prefactor corrected from $n^4$ to $2n^4$.}
  Status: $\checkmark$ RESOLVED. $B_n(u)/n^4 \leq 1+3/(2\pi-3) < 2$;
  corrected script recertifies [1,3] with min margin~91.3.

\item[C-18.] \textbf{Script renamed to \texttt{verify\_ia\_1\_to\_3.py}.}
  Status: $\checkmark$ DONE. SHA256: \texttt{1BB9E9DECF13580C...}

Then the "15 of 18" count becomes accurate with C-1..C-18 all listed.
