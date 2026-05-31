# Pólya Theorem RED ALERT Audit

## VERDICT: PÓLYA THEOREM MISSTATED

## The Problem

The paper's Theorem 1 states:

> Let K: ℝ → ℝ be even, satisfying:
> (i) K(t) > 0, (ii) K ∈ L¹, (iii) (log K)'' ≤ 0 for t ≥ 0,
> (iv) K(t) = O(e^{-|t|^{2+δ}}) for some δ > 0.
> Then F(z) = ∫ K(t) e^{izt} dt has only real zeros.

The function K(t) = e^{-|t|³} satisfies ALL FOUR conditions:
- (i) e^{-|t|³} > 0 ✓
- (ii) e^{-|t|³} ∈ L¹(ℝ) ✓
- (iii) (log e^{-|t|³})'' = -6|t| ≤ 0 ✓ (equals 0 only at t=0)
- (iv) e^{-|t|³} = O(e^{-|t|³}) with δ = 1 ✓

Yet by Csordas-Varga 1989 Example 2.1, its Fourier transform has
**infinitely many non-real zeros** (since 3 is not an even integer).

**The theorem as stated is FALSE.**

## The Resolution

Pólya's actual Theorem 2.2 (as stated in Csordas-Varga 1989) requires an
ADDITIONAL condition not present in our statement:

> K₁ must be **real analytic on an interval about the origin**.

This is the condition that distinguishes:
- e^{-t⁴} (real analytic at 0, only real zeros) ✓
- e^{-|t|³} (C^∞ but NOT real analytic at 0, has complex zeros) ✗

The function |t|³ is smooth but its Taylor series at 0 does not converge
to |t|³ in any neighborhood (it's identically 0 in the Taylor expansion
but |t|³ is not zero). Therefore e^{-|t|³} is NOT real analytic at t = 0.

## Impact on Our Proof

Our kernel Φ(u) = 4 Σ φₙ(u) is a convergent series of real-analytic
functions (exponentials and polynomials in e^u). The series converges
absolutely and uniformly on compact sets. Therefore Φ IS real analytic
on all of ℝ.

**The proof conclusion is NOT affected.** But the theorem statement
in the paper must be corrected to include the analyticity condition.

## Required Paper Fix

Add condition (v) to Theorem 1:

> (v) K is real analytic on a neighborhood of the origin.

Or more precisely, following Csordas-Varga 1989 Theorem 2.2:

> (v) K(t) = Σ cₖ tᵏ on (-r, r) for some r > 0.

Then add to the proof of the Main Result:

> Φ is real analytic on ℝ since it is defined by a uniformly convergent
> series of analytic functions.

## The e^{-t³} Discussion

The paper's current remark about e^{-t³} must be rewritten.
The current text says it "fails (iv)" which is WRONG (it satisfies
(iv) with δ=1). The correct statement is:

> e^{-|t|³} satisfies conditions (i)-(iv) but fails the analyticity
> condition: |t|³ is C^∞ but not real analytic at t = 0.

The computational finding (4 complex zeros) is still valuable as
a demonstration that the conditions are sharp.

## Risk Assessment: CRITICAL (but fixable)

The theorem is wrong as stated. Adding condition (v) fixes it.
Our kernel satisfies condition (v). The fix is a 2-line edit to
the paper. But this MUST be fixed before any journal submission.
