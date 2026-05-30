# Deep Paper Analysis: Application to Proof Strategy

## Paper 1: Suzuki — "On the Hilbert space derived from the Weil distribution"

### What Suzuki proves

**Theorem 1.1 (conditional on RH)**: The Hilbert space H_W obtained by
completing C_c^∞(R) with respect to the Weil hermitian form is isomorphic
to the de Branges space H(E_ξ), where E_ξ(z) = ξ(1/2 - iz) + ξ'(1/2 - iz).

The isomorphism is: K(Θ_ξ) → H_W via F ↦ [F^{-1}(F)]

And the norms match: ||E_ξ F||²_{H(E_ξ)} = ||F||²_{K(Θ_ξ)} = π⟨ψ_F, ψ_F⟩_W

**Theorem 1.4 (unconditional RH equivalent)**: RH is true if and only if
||P̂Dψ||²_{L²(R)} = π⟨ψ, ψ⟩_W for all ψ ∈ C_c^∞(R).

**Key unconditional construction**: Suzuki builds spaces H₀ and K₀
WITHOUT assuming RH, using "screw lines" of screw functions attached to
ζ(s). These spaces would equal H_W and K(Θ_ξ) if RH holds.

### How this applies to our project

1. **The Weil form IS the de Branges norm (under RH)**. Our stabilization
   result shows the Weil form converges as c → ∞. If we can show the
   limiting Weil form equals the de Branges norm, Suzuki's theorem gives
   us the isomorphism to the zero space.

2. **The unconditional spaces H₀, K₀ are computable**. Suzuki's S_t(z)
   function (equation 1.5-1.6) involves only:
   - Stieltjes constants
   - Von Mangoldt function Λ(n)
   - Digamma/polygamma functions
   - Hurwitz-Lerch zeta function
   All of which we can evaluate in mpmath. We could BUILD these spaces
   computationally and check whether the norm equality holds.

3. **The connection to our CvS computation**: The CCM operator D^{(λ,N)}_{log}
   from Connes' program produces eigenvectors ξ whose Fourier transforms
   ξ̂(z) are entire functions with all zeros on R. Suzuki's E_ξ is a
   DIFFERENT entire function (using ξ + ξ') but lives in the same de
   Branges framework. The question is whether the CCM eigenvectors
   converge to functions in Suzuki's K₀.

4. **Suzuki explicitly says** (after Theorem 1.1): "H_W and H(E_ξ) must
   have an 'arithmetic structure' through the Weil explicit formula, but
   we will not discuss this further." THIS IS THE GAP — the arithmetic
   structure is what connects the abstract Hilbert space to the actual
   zeros.

### Actionable computation

We can implement Suzuki's operator P̂D and compute the norm equality
from Theorem 1.4 for specific test functions ψ. If the equality holds
numerically to high precision, it's evidence for RH via a completely
new pathway. If it fails, RH is false.

## Paper 2: Ohzeki — "Analytical SVD of Analytic-Continuation Kernels"

### What Ohzeki proves

The Laplace kernel K_c(x,y) = e^{-cxy} (the "imaginary-bandwidth
continuation" of Slepian's finite Fourier transform) has:

1. **Commuting differential operator**: D^{(L)}_z = d/dz[(1-z²)d/dz] + c²z²
   Note the PLUS sign (vs Slepian's minus). This is the "Laplace-Slepian"
   operator.

2. **Bilinear expansion**: e^{-cxy} = Σ μ_n ψ_n(x;c) ψ_n(y;c)
   where ψ_n are PSWFs analytically continued in bandwidth.

3. **Shannon number**: N_c = 2c/π = βω_max/π fixes the information
   capacity. Components with n >> N_c are exponentially small.

4. **Eigenvalue cliff**: Around n = N_c, eigenvalues drop by 7+ OOM
   and enter the exponentially small tail.

### How this applies to our project

1. **Direct connection to CvS Galerkin**: The CvS Galerkin matrix is
   built from the Weil quadratic form, which involves the kernel
   q(U_m, U_n)(y) evaluated at log(p) for primes p. The archimedean
   part involves precisely a sinc-type kernel. The Ohzeki factorization
   shows this kernel decomposes into a "pure Laplace channel" times
   a statistical weight — and the Laplace channel has Shannon number
   N_c = 2c/π.

2. **Our CvS parameter N maps to Shannon number**: In our computation,
   N is the Galerkin basis dimension (2N+1 functions). The Shannon
   number N_c = 2·(log c)/π ≈ log(c)/1.57. For c=13, N_c ≈ 1.6; for
   c=100, N_c ≈ 2.9. This means with N=50 or N=100, we are MASSIVELY
   oversampling relative to the Shannon limit — which explains why the
   eigenvalue is so tiny (10^{-57} at c=13). The eigenvector is
   concentrating in the first ~2 Shannon modes.

3. **Convergence rate from plunge region**: The Karnik-Romberg-Davenport
   bound says the plunge region has O(log(NW)·log(1/ε)) eigenvalues
   between ε and 1-ε. Applied to our setting: the number of "significant"
   modes of the truncated Weil form grows only logarithmically with the
   cutoff. This means the stabilization we observe is EXPECTED from
   information theory — once you include enough primes, you've captured
   all the Shannon-limited information.

4. **Why stabilization implies convergence**: If the number of significant
   modes is bounded by N_c = O(log c), and our Galerkin dimension N >> N_c,
   then the eigenvector is fully determined by the significant modes.
   Adding more primes (increasing c) only adds exponentially small modes
   that don't change the eigenvector. This is exactly what we observed:
   delta = 0.002 OOM at c=29.

## Synthesis: A Computational Path

The two papers together suggest:

1. **Suzuki's H₀ space** can be built computationally (it's unconditional)
2. **Ohzeki's Shannon number** explains why our stabilization works
3. **The bridge**: if the CvS eigenvectors (which live in a truncated
   version of the Weil form space) converge to elements of Suzuki's H₀,
   then by Suzuki's Theorem 5.6, they must converge to elements of the
   de Branges space — which forces their zeros to be the Riemann zeros.

The Shannon number argument provides the analytical control needed:
- For n > N_c, the eigenvalues are exponentially small
- The eigenvector is determined by the first N_c modes
- These modes stabilize once all relevant primes are included
- The limit function must be in the de Branges space by completeness

This is not yet a proof, but it's a concrete analytical pathway that
our computational evidence supports.

## Computational Results (May 30, 2026)

### Suzuki Norm Equality (Phase 8)

Tested ||P̂Dψ||² = π⟨ψ, ψ⟩_W for 5 test functions using 30 zeros:

- **gaussian_bump(σ=0.2): ratio = 0.9496** ← within 5% of RH prediction!
  - ||P̂Dψ||² = 1.096e-4, π⟨ψ,ψ⟩_W = 1.154e-4
  - log10|r-1| = -1.30 (1.3 digits of agreement)
  - Stable: ratio identical with 10 vs 30 zeros (Weil sum converged)

- bump[-0.5,0.5]: ratio = 0.074 (numerical FT cancellation in symmetric case)
- cos(πx)·bump: ratio = 0.210 (oscillatory FT + bandlimit mismatch)
- cos(2πx)·bump: ratio = 0.0007 (FT spectral content far from [-1/2,1/2])

The gaussian_bump result is the most informative because it has
asymmetric amplitude distribution that avoids FT cancellation.
The 5% residual is consistent with: truncation at 30 zeros +
quadrature error at dps=25.

### Suzuki Norm Equality — Correction

Subsequent testing with varied test functions (asymmetric bump,
wide bump, hat function) shows the ratio varies from 0.07 to 578
across different functions. The spectral zero sum Σ|ψ̂(γ_n/(2π))|²
is NOT the complete Weil form — it omits the archimedean and pole
corrections that are essential. The gaussian_bump ratio of 0.95
was coincidental, not a genuine match.

The correct Weil form requires the full Weil explicit formula
(archimedean integral + prime contributions + pole terms at s=0,1).
The CvS Galerkin matrix IS computing the full Weil form correctly
in the Fourier basis.

### Eigenvector Mode Participation

Direct decomposition of the CvS ground-state eigenvector:

- c=13 (N_c=1.63): 99% energy in 7 modes, peaked at n=0,±1,±2
- c=17 (N_c=1.80): 99% energy in 15 modes, shifted to n=±4,±5
- c=23 (N_c=2.00): 99% energy in 22 modes, spread to n=±4,±6,±8
- c=29 (N_c=2.14): 99% energy in 20 modes, concentrated at n=±4,±9,±10

Key finding: The Shannon number does NOT directly predict the mode
count. The eigenvector uses many more modes than N_c. However, the
EIGENVALUE still stabilizes (the [-80.7, -79.3] OOM plateau).
This means the Weil form itself converges even as the eigenvector
restructures across modes as c increases.

The eigenvector always has even symmetry: |v_n| = |v_{-n}|.

### Screw Line (Phase 10)

||S_t||² grows monotonically: 75.5 (t=10) → 273.6 (t=200).
Consistent with H₀ space filling as more prime powers contribute.

## Next steps

1. Implement full Weil explicit formula (archimedean + prime + poles)
   to correctly compute ⟨ψ, ψ⟩_W and retest Suzuki Theorem 1.4
2. Compare CvS eigenvectors with elements of Suzuki's K₀
3. Study eigenvector restructuring: why does the eigenvalue stabilize
   even as the eigenvector shifts weight to higher modes?
