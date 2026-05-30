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

## New Bridge Pathway (May 2026)

### Suzuki (2025): Unconditional RH Equivalent

**Theorem 1.4**: RH ⟺ ||P̂Dψ||²_{L²(ℝ)} = π⟨ψ, ψ⟩_W for all ψ ∈ C_c^∞(ℝ)

This gives us an RH-equivalent condition that is COMPUTABLE on both sides:
- LHS (Paley-Wiener norm): unconditional, pure Fourier analysis
- RHS (Weil form): the same quantity our CvS Galerkin measures

**Unconditional spaces H₀, K₀**: Suzuki constructs these WITHOUT assuming
RH, using screw functions S_t(z). Under RH, H₀ = H_W. The question is
whether CvS eigenvectors converge to elements of H₀.

Implemented in: `src/riemann/suzuki.py`, tested by `run_bridge.py` Phase 8.

### Ohzeki (2026): Shannon Number and Convergence Rate

The Laplace-Slepian kernel has Shannon number N_c = 2·log(c)/π.
This explains our form stabilization:
- For c=13: N_c ≈ 1.63 (only ~2 significant modes)
- For c=47: N_c ≈ 2.45 (only ~3 significant modes)
- With N=100 basis functions, we oversample by 40-60x
- Eigenvector is fully determined by first ~N_c modes
- Adding more primes adds only exponentially small tail modes

The Karnik-Romberg-Davenport (2021) bounds quantify the convergence:
the plunge region has O(log(N_c)·log(1/ε)) eigenvalues, providing the
non-asymptotic control needed for Connes' step 6.5.

Implemented in: `src/riemann/shannon.py`, tested by `run_bridge.py` Phase 9.

### The Bridge

1. CvS eigenvectors live in truncated Weil form space
2. Shannon number bounds show they stabilize after ~N_c modes
3. Suzuki's Theorem 5.6: stable elements must converge to H₀
4. If CvS eigenvectors → H₀, and H₀ = de Branges space (under RH),
   then eigenvector zeros → Riemann zeros
5. Suzuki's Theorem 1.4 provides a direct numerical test

## Key Insight for Our Approach

The most promising path combines:
- **Connes' spectral construction** (the framework)
- **Groskin's computational infrastructure** (the verification)
- **Suzuki's norm equality** (the RH-equivalent test)
- **Ohzeki's Shannon theory** (the convergence rate control)

The convergence gap is addressed by the Shannon number argument:
once N >> N_c, the eigenvector is information-theoretically determined.
The identification gap is addressed by Suzuki's norm equality: if
||P̂Dψ||² = π⟨ψ, ψ⟩_W, the limit must be in the de Branges space.
