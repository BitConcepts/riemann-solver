# Deliverable: certificate_hash_formatting_fix.md
# Task 8 — Fix Certificate Hash Table Formatting

## Option B (recommended): Label as prefixes explicitly

Change the column header from:
  "SHA256 (full 64 hex, see docs/certificate_hash_table.md)"

To:
  "SHA256 prefix (16 chars); full hashes in docs/certificate\_hash\_table.md"

Then add below the table:
> The SHA256 column shows 16-character prefixes for readability. Full 64-character
> hashes are in \texttt{docs/certificate\_hash\_table.md}. Updated certificate for
> \texttt{verify\_ia\_1\_to\_3.json}: \texttt{1BB9E9DECF13580C...}

## Full updated hashes

C4  (verify_logconcavity_rigorous.json): 0D0841DAB32396D9...
C4b (verify_logconcavity_arb.json):      974B67CC58B96117...
C5  (verify_ia_1_to_3.json):             1BB9E9DECF13580C...  [NEW — corrected epsilon]
Main (proof_certificate_v2.json):        8B538345D589638A...
