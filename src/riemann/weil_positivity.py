"""Weil positivity criterion and Connes-van Suijlekom Galerkin matrix.

Implements the truncated Weil operator Q(c) from restricted Euler
products over primes p ≤ c. The ground-state eigenvalue λ_min(c)
encodes proximity to Weil positivity (which implies RH).

References:
    - Connes, Consani & Moscovici (2025), arXiv:2511.22755
    - Groskin (2026), connes-cvs package, Zenodo 10.5281/zenodo.19546515
    - Weil (1952), explicit formulas
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


def _primes_up_to(c: int) -> list[int]:
    """Simple sieve of Eratosthenes up to c."""
    if c < 2:
        return []
    sieve = [True] * (c + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(c**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, c + 1, i):
                sieve[j] = False
    return [i for i in range(2, c + 1) if sieve[i]]


@dataclass
class GalerkinResult:
    """Result of a CvS Galerkin matrix computation."""

    cutoff: int  # prime cutoff c
    n_basis: int  # basis dimension N
    lambda_min: mp.mpf  # ground-state eigenvalue
    gamma1_approx: mp.mpf | None  # approximation to first zero
    gamma1_error: mp.mpf | None  # |γ₁_approx - γ₁_exact|


def _archimedean_kernel(n: int, m: int, L: mp.mpf) -> mp.mpf:
    """Compute the archimedean contribution to the Galerkin matrix entry Q_{n,m}.

    This is the integral involving the Euler-Mascheroni constant and
    digamma function contributions.

    Simplified version — full implementation would follow Groskin (2026).
    """
    if n == m:
        return 2 * (1 - abs(n) * mp.pi / L) if abs(n) * mp.pi < L else mp.mpf(0)
    else:
        n_val = mp.mpf(n)
        m_val = mp.mpf(m)
        return (mp.sin(2 * mp.pi * m_val / L) - mp.sin(2 * mp.pi * n_val / L)) / (
            mp.pi * (n_val - m_val)
        )


def build_galerkin_matrix(
    c: int,
    N: int = 50,
    T: int = 200,
    dps: int = 80,
) -> mp.matrix:
    """Build the CvS Galerkin matrix Q(c) at prime cutoff c.

    This is a simplified scaffold implementation. The full version
    requires careful handling of the archimedean integral (digamma-based)
    and non-archimedean (prime) contributions per Proposition 4.1 of
    Connes-van Suijlekom (2025).

    Args:
        c: prime cutoff (use primes ≤ c in the Euler product)
        N: basis dimension (2N+1 basis functions)
        T: truncation parameter for integrals
        dps: decimal precision

    Returns:
        (2N+1) × (2N+1) mpmath matrix
    """
    with mp.workdps(dps):
        primes = _primes_up_to(c)
        L = mp.log(mp.mpf(c))
        dim = 2 * N + 1

        Q = mp.matrix(dim, dim)

        # Archimedean contribution (simplified)
        for i in range(dim):
            n = i - N
            for j in range(dim):
                m = j - N
                Q[i, j] = _archimedean_kernel(n, m, L)

        # Non-archimedean contributions from each prime
        for p in primes:
            log_p = mp.log(mp.mpf(p))
            for i in range(dim):
                n = i - N
                for j in range(dim):
                    m = j - N
                    # Weil quadratic form contribution from prime p
                    # W_p adds log(p) * Σ_{k=1}^∞ (f(p^k) + f♯(p^k))
                    # Simplified: first-order contribution
                    phase = (n - m) * log_p / L
                    Q[i, j] -= log_p * mp.cos(2 * mp.pi * phase) / mp.sqrt(mp.mpf(p))

    return Q


def compute_ground_state(Q: mp.matrix) -> tuple[mp.mpf, mp.matrix]:
    """Diagonalize Q and return (λ_min, eigenvector).

    Uses mpmath's eigsy for symmetric eigendecomposition.
    """
    # Symmetrize
    n = Q.rows
    Qs = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            Qs[i, j] = (Q[i, j] + Q[j, i]) / 2

    eigenvalues, eigenvectors = mp.eigsy(Qs)

    # Find minimum eigenvalue
    min_idx = 0
    min_val = eigenvalues[0]
    for i in range(1, len(eigenvalues)):
        if eigenvalues[i] < min_val:
            min_val = eigenvalues[i]
            min_idx = i

    eigvec = eigenvectors[:, min_idx]
    return mp.mpf(min_val), eigvec


def run_galerkin(c: int, N: int = 50, dps: int = 80) -> GalerkinResult:
    """Full pipeline: build matrix, diagonalize, extract results."""
    with mp.workdps(dps):
        Q = build_galerkin_matrix(c, N, dps=dps)
        lam_min, _ = compute_ground_state(Q)

        # Known first zero for comparison
        _gamma1_exact = mp.mpf("14.134725141734693790457251983562470270784257115699")  # noqa: F841

        return GalerkinResult(
            cutoff=c,
            n_basis=2 * N + 1,
            lambda_min=lam_min,
            gamma1_approx=None,  # TODO: extract from eigenvector
            gamma1_error=None,
        )
