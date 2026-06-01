# Deliverable: appendix_b_hash_table_fix.md

## Problem
Table header says "full 64 hex, see docs/..." but only shows 16-char prefixes.

## Fix
Change header column:
OLD: "SHA256 (full 64 hex, see \texttt{docs/certificate\_hash\_table.md})"
NEW: "SHA256 prefix (16 hex); full in \texttt{docs/certificate\_hash\_table.md}"

Add note below table:
"Prefixes shown for readability; full 64-character hashes in 
\texttt{docs/certificate\_hash\_table.md}."
