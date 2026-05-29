"""Spectral operator construction for the Riemann Hypothesis.

Implements the rank-one perturbation of the scaling operator on [λ⁻¹, λ]
whose spectrum approximates the non-trivial zeros of ζ(1/2 + is).

References:
    - Connes, Consani & Moscovici (2025), arXiv:2511.22755 (Theorem 1.1)
    - Hilbert-Pólya conjecture: zeros are eigenvalues of a self-adjoint operator
"""

from __future__ import annotations

import mpmath as mp


def scaling_operator_eigenvalues(N: int, L: mp.mpf) -> list[mp.mpf]:
    """Eigenvalues of the scaling operator D^(λ)_log on [λ⁻¹, λ].

    D_log has eigenvalues nπ/log(λ) for n ∈ ℤ with |n| ≤ N.
    Here L = log(λ).
    """
    return [mp.mpf(n) * mp.pi / L for n in range(-N, N + 1)]


def build_spectral_operator(
    lam: float | mp.mpf,
    N: int,
    dps: int = 80,
) -> mp.matrix:
    """Build the rank-one perturbation D^(λ,N)_log.

    This is a scaffold for the Connes-Consani-Moscovici construction.
    The full implementation requires:
    1. The Weil quadratic form QW^N_λ restricted to E_N
    2. Finding the smallest eigenvalue ε_N and eigenvector ξ
    3. Constructing D_log - |D_log ξ⟩⟨δ_N|

    Returns the matrix representation in the E_N basis.
    """
    with mp.workdps(dps):
        L = mp.log(mp.mpf(lam))
        dim = 2 * N + 1

        # Start with diagonal scaling operator
        D = mp.matrix(dim, dim)
        for i in range(dim):
            n = i - N
            D[i, i] = mp.mpf(n) * mp.pi / L

        # TODO: Add rank-one perturbation from Weil quadratic form
        # This requires the full Weil QF computation

    return D
