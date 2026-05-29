# Proof Strategy — State of the Art and Actionable Gaps

## Executive Summary

As of May 2026, the Connes spectral program is the most advanced
proof framework for RH. The precise remaining gap is well-defined:

> **Prove that the regularized determinants det_reg(D^(λ,N)_log − z)
> converge to the Riemann Ξ function as N, λ → ∞.**

This single convergence statement, if established rigorously, would
complete the proof of the Riemann Hypothesis (Connes-Consani-Moscovici
2025, §7-§8).

---

## Current Landscape (harvested May 2026)

### Tier 1: Connes Program (closest to proof)

**Connes (Feb 2026)** — arXiv:2602.04022 "Past, Present and a Letter Through Time"
- Survey + new results using only math Riemann knew + modern computers
- Using primes ≤ 13, obtains first 50 zeros with accuracy 10^{-55} to 10^{-3}
- Proves ALL approximating zeros lie exactly on the critical line
- Section 6.6 "Remaining steps" explicitly lists what's needed for proof
- Connection to prolate spheroidal wave functions and information theory

**Connes-Consani-Moscovici (Nov 2025)** — arXiv:2511.22755 "Zeta Spectral Triples"
- **Theorem 1.1**: Self-adjoint operators D^(λ,N)_log whose spectra are ALL real
- Regularized determinant ξ_hat(z) is entire with all zeros on real line
- §8: Explicitly lists the "missing steps"
- Strategy: show det_reg → Ξ function via prolate wave function theory

**Groskin (May 2026)** — arXiv:2605.20224 "High-Precision Approximation"
- First independent reproduction of CvS Galerkin at 16 cutoffs (c=13..100)
- 329 matching digits on γ₁ at c=100, N=250, dps=500
- 113 OOM convergence across 15 cutoffs
- Aitken extrapolation approaches Connes §6.4 prediction to within 3.3 OOM
- connes-cvs package: MIT-licensed, pip-installable

### Tier 2: Even Dominance (claimed proof, submitted)

**Geiger (Mar 2026)** — Zenodo 10.5281/zenodo.19035640
- Three-part series: Foundations → Even Dominance → Conclusio
- Claims proof via Connes' Theorem 6.1 + Hurwitz sufficiency + Even dominance
- 33 computer-assisted certificates (interval arithmetic, mpmath.iv)
- Three-regime bridge: CAP for λ∈[100,1.3M], PNT Transfer for λ≥442k
- **Submitted to Communications in Mathematics (2026-03-27)**
- Status: under peer review — NOT yet accepted

### Tier 3: Various Zenodo/preprint claims (unverified)

Multiple claimed proofs posted on Zenodo (A.I. Visions LTD, Paltoo,
Priest, Meghani, Ducci, etc.). None peer-reviewed. Most have obvious
gaps or circular reasoning when examined closely.

---

## The Exact Proof Gap (Connes program)

From CCM 2025 §8 and Connes 2026 §6.6, the missing steps are:

### Step 1: Convergence of k_λ to k (the eigenvector limit)
The truncated eigenvector k_λ (ground state of QW^N_λ) must converge
to the continuum Weil minimizer k as λ → ∞. This requires:
- **Sobolev regularity**: s(c) ≈ 55·log(c) - 128 (empirically measured)
- **Eigenvector c-invariance**: overlap ≥ 0.95 across all 105 cutoff pairs
  (Groskin 2026 confirms this)

### Step 2: Convergence of Fourier transforms k̂_λ → k̂
The Fourier-Mellin transforms of the eigenvectors must converge
uniformly on compact subsets of ℂ. Since k̂_λ has all zeros on ℝ
(by Theorem 1.1(iii)), and if the limit k̂ equals Ξ, then Hurwitz's
theorem forces all zeros of Ξ to be real → RH.

### Step 3: Identification k̂ = Ξ (the Riemann Ξ function)
The limit function must actually be the Ξ function, not some other
entire function with real zeros. This requires:
- Matching the functional equation
- Matching the Hadamard product
- Or: matching finitely many zeros + growth order determines Ξ uniquely

### Connection to Prolate Spheroidal Wave Functions
Connes 2026 §6.3 identifies a deep link: the truncated eigenvectors
are approximated by prolate spheroidal wave functions (Slepian).
The convergence question reduces to:
- The prolate wave operator's eigenvalues cluster near 0 and 1
- The "band-limited ≈ time-limited" phenomenon of information theory
  provides the analytical handle

---

## CPSC as Proof Modeler

The CPSC paradigm can model the proof obligation structure:

**Constraint Architecture for the Proof:**
```
constraint_architecture:
  - type: spectral_reality
    constraint: "All eigenvalues of D^(λ,N)_log are real"
    status: PROVEN (Theorem 1.1, Carathéodory-Fejér)

  - type: eigenvector_convergence
    constraint: "k_λ converges in Sobolev norm as λ → ∞"
    status: EMPIRICALLY_SUPPORTED (Groskin: s(c) grows, overlap ≥ 0.95)
    gap: RIGOROUS_BOUND_NEEDED

  - type: fourier_convergence
    constraint: "k̂_λ → Ξ uniformly on compact sets"
    status: EMPIRICALLY_SUPPORTED (329 digits at c=100)
    gap: UNIFORM_CONVERGENCE_PROOF_NEEDED

  - type: limit_identification
    constraint: "The limit function equals the Riemann Ξ function"
    status: OPEN
    gap: FUNCTIONAL_EQUATION_MATCHING
```

**DoF vector**: The proof has 3 remaining degrees of freedom (Steps 1-3).
**Projection**: Each step can be "projected" from empirical evidence
toward rigorous proof by:
1. Establishing explicit error bounds
2. Proving monotonicity of convergence
3. Using the prolate wave function framework for analytical control

---

## Actionable Work Items

### Immediate (this project can do)

1. **Install connes-cvs** and reproduce Groskin's results
2. **Extend to c=100** and verify the 329-digit γ₁ extraction
3. **Measure eigenvector convergence rate** quantitatively
4. **Test even dominance** at specific λ values (Geiger's approach)
5. **Implement prolate spheroidal wave functions** as the analytical bridge

### Medium-term (requires mathematical insight)

6. **Derive explicit Sobolev regularity bounds** for k_λ
7. **Prove uniform convergence** of k̂_λ on compact sets using
   the information-theoretic connection
8. **Identify the limit function** with Ξ via the Hadamard product

### Prize-level (the actual proof)

9. Close Steps 1-3 rigorously
10. Write the proof manuscript
11. Submit to Annals of Mathematics or equivalent
12. Withstand 2+ years of peer review

---

## Key Insight for Our Approach

The most promising path combines:
- **Connes' spectral construction** (the framework)
- **Groskin's computational infrastructure** (the verification)
- **Geiger's even-dominance certificates** (the computer-assisted rigor)
- **CPSC constraint-projection** (modeling the proof structure)

The convergence gap is the bottleneck. The prolate wave function
connection (Slepian theory) may provide the analytical handle.
This is where focused effort should go.
