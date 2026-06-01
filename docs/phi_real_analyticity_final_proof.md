# Deliverable: phi_real_analyticity_final_proof.md
# Task 1 — Φ Analyticity: Local Real Analyticity on ℝ

## Summary

The paper requires Φ to be **real analytic on ℝ** (Pólya condition (v): real analytic on a
neighborhood of the origin; in fact our proof gives all of ℝ). The proof is valid and
complete. The existing proof sketch in Proposition 3 is correct but its wording risks
implying Φ is *entire* (holomorphic on all of ℂ), which is **false**.

This document provides the corrected, fully explicit proof that should replace the current
parenthetical in Proposition 3(v).

---

## Why "entire" is wrong for Φ

Each φ_n(z) = (2π²n⁴e^{9z/2} − 3πn²e^{5z/2}) · e^{−πn²e^{2z}} is indeed entire in z.
But the *series* Σ φ_n(z) does NOT converge uniformly on every compact subset of ℂ.

On a compact set containing points with Re(e^{2z}) ≤ 0 (e.g., z = iπ/2 where e^{2z} = −1),
the factor e^{−πn²e^{2z}} = e^{+πn²} grows without bound. The series diverges at such points.
So Φ is **not entire**.

The paper must claim only: **Φ is real analytic on ℝ**.

---

## Corrected Proof (Local Real Analyticity)

**Proposition.** *The function Φ defined by (3) is real analytic on ℝ.*

**Proof.** Fix any point u₀ ∈ ℝ. We show Φ is holomorphic on a complex disk of radius r
centered at u₀, which implies real analyticity at u₀. Since u₀ is arbitrary, Φ is real
analytic on all of ℝ.

**Step 1: Choose r.** Take r = π/8. For any z = x + iy with |z − u₀| < r:
  - |Im(2z)| = 2|y| ≤ 2r = π/4
  - Therefore cos(2 Im z) ≥ cos(π/4) = 1/√2 > 0

**Step 2: Bound on the exponential factor.** Write e^{2z} = e^{2x}(cos(2y) + i sin(2y)).
The real part is Re(e^{2z}) = e^{2x} cos(2y). For |z − u₀| < r:
  - x = Re(z) ∈ (u₀ − r, u₀ + r), so e^{2x} ≥ e^{2(u₀−r)}
  - cos(2y) ≥ 1/√2
  - Therefore Re(e^{2z}) ≥ c := e^{2(u₀−r)}/√2 > 0

**Step 3: Bound |φ_n(z)|.** For z in the disk |z − u₀| ≤ r/2 (a compact subdisk):

For the prefactor: |e^{kz}| ≤ e^{k|z|} ≤ e^{k(|u₀|+r)} for k ∈ {5/2, 9/2}, so
  |2π²n⁴e^{9z/2} − 3πn²e^{5z/2}| ≤ A n⁴,  where A = A(u₀, r) is a finite constant.

For the exponential: |e^{−πn²e^{2z}}| = e^{−πn² Re(e^{2z})} ≤ e^{−πn²c/2}  
(using the subdisk Re(e^{2z}) ≥ c' = e^{2(u₀−3r/2)}/√2 > c/2 for the smaller disk).

Therefore |φ_n(z)| ≤ A n⁴ · e^{−πn²c/2} =: Mₙ  uniformly on |z − u₀| ≤ r/2.

**Step 4: Convergence.** Since Σ Mₙ = A · Σ n⁴ e^{−πcn²/2} < ∞ (standard: n⁴e^{−αn²} is
summable for any α > 0), the Weierstrass M-test gives uniform convergence of Σ φ_n on
|z − u₀| ≤ r/2. A uniform limit of holomorphic functions is holomorphic (Weierstrass theorem
for analytic functions).

**Conclusion.** Φ is holomorphic on the complex disk |z − u₀| < r/2 for every u₀ ∈ ℝ.
In particular it is real analytic at u₀. ∎

---

## Paper Change Required

**Replace in Proposition 3, property (v) proof:**

Old text:
> For (v): each φ_n is entire (a product of exponentials), and the series (3) converges
> uniformly on compacts by the Weierstrass M-test.

New text:
> For (v): Φ is real analytic on ℝ. Fix any u₀ ∈ ℝ. For r = π/8, any z in the disk
> |z − u₀| < r satisfies Re(e^{2z}) ≥ e^{2(u₀−r)}/√2 =: c > 0, bounding each term by
> |φ_n(z)| ≤ A n⁴ e^{−πcn²/2} uniformly on the half-disk. Since Σ n⁴e^{−πcn²/2} < ∞, the
> Weierstrass M-test gives uniform convergence of the series to a holomorphic function on
> that disk; hence Φ is real analytic at u₀. Since u₀ was arbitrary, Φ is real analytic
> on ℝ.

---

## Acceptance Criterion Status

✓ The proof establishes exactly the property required by Pólya condition (v): real analyticity
  on a neighborhood of the origin (in fact on all of ℝ).
✓ "Entire" is not claimed or implied.
✓ The argument is local (per point u₀) and then extended by arbitrariness.
✓ No overclaiming: the failure of convergence at complex points like z = iπ/2 is consistent
  with the proof, which only works on disks where Re(e^{2z}) > 0.
