# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""High-precision Riemann zeta function wrappers.

Wraps mpmath for arbitrary-precision evaluation of ζ(s) and related
functions. All functions respect the current mpmath precision context.

References:
    - mpmath documentation: https://mpmath.readthedocs.io/
    - Edwards (2001), Riemann's Zeta Function
"""

from __future__ import annotations

import mpmath as mp


def zeta(s: complex | mp.mpf | mp.mpc, dps: int | None = None) -> mp.mpc:
    """Evaluate the Riemann zeta function ζ(s) to `dps` decimal places.

    Uses mpmath's hybrid algorithm: Borwein for s near real line,
    Riemann-Siegel for large imaginary part, Euler-Maclaurin otherwise.
    """
    if dps is not None:
        with mp.workdps(dps):
            return mp.zeta(s)
    return mp.zeta(s)


def zeta_derivative(s: complex | mp.mpf | mp.mpc, n: int = 1) -> mp.mpc:
    """Compute the n-th derivative ζ^(n)(s)."""
    return mp.zeta(s, derivative=n)


def hardy_z(t: float | mp.mpf) -> mp.mpf:
    """Evaluate the Hardy Z-function Z(t).

    Z(t) = e^{iθ(t)} ζ(1/2 + it) is real for real t.
    Sign changes of Z(t) locate zeros on the critical line.
    """
    return mp.siegelz(t)


def hardy_z_derivative(t: float | mp.mpf, n: int = 1) -> mp.mpf:
    """Compute the n-th derivative of Z(t)."""
    return mp.siegelz(t, derivative=n)


def siegel_theta(t: float | mp.mpf) -> mp.mpf:
    """Evaluate the Riemann-Siegel theta function θ(t).

    θ(t) = Im(log Γ(1/4 + it/2)) - (t/2) log π
    """
    return mp.siegeltheta(t)


def gram_point(n: int) -> mp.mpf:
    """Compute the n-th Gram point g_n where θ(g_n) = nπ."""
    return mp.grampoint(n)


def eta(s: complex | mp.mpf | mp.mpc) -> mp.mpc:
    """Evaluate the Dirichlet eta function η(s) = (1 - 2^{1-s}) ζ(s).

    Unlike ζ, the eta function is entire (no pole at s=1).
    """
    return mp.altzeta(s)


def nzeros(t: float | mp.mpf) -> int:
    """Estimate the number of zeros of ζ with 0 < Im(ρ) < t.

    Uses the Riemann-von Mangoldt formula:
        N(t) ≈ (t/2π) log(t/2πe) + 7/8
    """
    return mp.nzeros(t)


def stieltjes_constant(n: int) -> mp.mpf:
    """Compute the n-th Stieltjes constant γ_n.

    These appear in the Laurent expansion of ζ(s) about s=1:
        ζ(s) = 1/(s-1) + Σ (-1)^n/n! γ_n (s-1)^n
    """
    return mp.stieltjes(n)


def set_precision(dps: int) -> None:
    """Set the global decimal precision for all computations."""
    mp.mp.dps = dps


def get_precision() -> int:
    """Get the current decimal precision."""
    return mp.mp.dps
