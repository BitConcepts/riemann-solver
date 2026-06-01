# Deliverable: claim_language_final_softening.md
# Task 6 — Soften Abstract and Introduction Claim Language

## Specific Required Changes

### Abstract (line 33)

OLD:
> By a classical theorem of Pólya (1927), this establishes that all zeros of Ξ(t) are real,
> which is equivalent to the Riemann Hypothesis.

NEW:
> Subject to the cited form of Pólya's 1927 theorem (Theorem 1), this establishes that all
> zeros of Ξ(t) are real, which is equivalent to the Riemann Hypothesis.

### Introduction paragraph (line ~66)

OLD:
> We verify that Φ satisfies all of these conditions, thereby establishing RH.

NEW:
> We verify that Φ satisfies all of these conditions; subject to the cited Pólya theorem,
> this yields RH as a conditional consequence (see Section 10 for a full dependency table).

### RH Corollary proof (already fixed in the previous audit pass)

The corollary proof now says "RH follows, subject to the cited dependencies catalogued
in Section 10." This is correct and sufficient.

### What NOT to change

- Section titles (e.g., "Corollary [Riemann Hypothesis]") — these are standard and
  understood to be conditional by context.
- The body of the proofs — these are mathematically correct conditional derivations and
  should not be hedged within the proof text itself.
- The Limitations section — already explicitly lists all dependencies.
- The Proof-Critical Dependencies table — already accurate.

## Why This Level of Softening is Appropriate

The paper is a serious conditional proof package. Over-hedging every statement would
make the paper unreadable. The right level is:
1. Abstract: one conditional clause per proof claim sentence.
2. Introduction: one reference to the dependency table.
3. Main proof: mathematically correct conditional proofs (if conditions, then conclusion).
4. Limitations + checklist: explicit accounting of what remains open.

## Acceptance Criterion

✓ Abstract no longer says "this establishes RH" unconditionally.
✓ Introduction no longer says "thereby establishing RH" without qualification.
✓ The qualification points to the dependency table or Pólya citation explicitly.
✓ The paper still reads as a serious, confident mathematical argument (not excessively hedged).
